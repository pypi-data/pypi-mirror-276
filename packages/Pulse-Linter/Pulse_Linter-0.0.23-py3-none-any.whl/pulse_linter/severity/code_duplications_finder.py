import ast
import os
import sys
import argparse
from collections import defaultdict
from enum import Enum


class ReturnCode(Enum):
    SUCCESS = 0
    BAD_INPUT = 1
    THRESHOLD_EXCEEDED = 2


class DuplicationFinder:

    def __init__(self):
        self.overall_score = None

    def get_all_codes_from_dir(self, directory, file_extensions):
        source_code_files = []
        for dirpath, _, filenames in os.walk(directory):
            for name in filenames:
                _, file_extension = os.path.splitext(name)
                if file_extension[1:] in file_extensions:
                    filename = os.path.join(dirpath, name)
                    source_code_files.append(filename)
        print(f"Found {len(source_code_files)} source code files in {directory}: {source_code_files}")
        return source_code_files

    def parse_source_code(self, file_path):
        with open(file_path, 'r', errors='ignore') as file:
            source_code = file.read()
        return ast.parse(source_code, filename=file_path)

    def extract_function_def_and_bodies(self, tree):
        functions = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                function_name = node.name
                function_body = ast.unparse(node)
                functions[function_name] = function_body
        return functions

    def compare_function_bodies(self, f1_bodies, f2_bodies):
        common_functions = set(f1_bodies.keys()).intersection(f2_bodies.keys())
        similar_bodies_count = sum(1 for func in common_functions if f1_bodies[func] == f2_bodies[func])
        similarity = len(common_functions) / max(len(f1_bodies), len(f2_bodies))
        body_similarity = similar_bodies_count / max(len(f1_bodies), len(f2_bodies))
        return similarity, body_similarity

    def compute_similarity_level(self, similarity):
        if similarity <= 0.33:
            return "Low"
        elif similarity <= 0.66:
            return "Medium"
        else:
            return "High"

    def compute_overall_score(self, code_similarity):
        total_similarity = 0
        for similarities in code_similarity.values():
            for _, (name_similarity, body_similarity) in similarities.items():
                total_similarity += (name_similarity + body_similarity) / 2
        self.overall_score = total_similarity / len(code_similarity)

    def run(self, fail_threshold, directories):
        source_code_files = []
        if directories:
            for directory in directories:
                if not os.path.isdir(directory):
                    print("Path does not exist or is not a directory:", directory)
                    return (ReturnCode.BAD_INPUT, {})
                source_code_files += self.get_all_codes_from_dir(directory, ['py'])
        else:
            print("No directories provided.")
            return (ReturnCode.BAD_INPUT, {})

        if len(source_code_files) < 2:
            print("Not enough source code files found")
            return (ReturnCode.BAD_INPUT, {})

        code_similarity = defaultdict(dict)
        for i, file1 in enumerate(source_code_files):
            for file2 in source_code_files[i + 1:]:
                tree1 = self.parse_source_code(file1)
                tree2 = self.parse_source_code(file2)
                f1_functions = self.extract_function_def_and_bodies(tree1)
                f2_functions = self.extract_function_def_and_bodies(tree2)
                name_similarity, body_similarity = self.compare_function_bodies(f1_functions, f2_functions)
                code_similarity[file1][file2] = (name_similarity, body_similarity)

        exit_code = ReturnCode.SUCCESS
        for file1, similarities in code_similarity.items():
            for file2, (name_similarity, body_similarity) in similarities.items():
                if name_similarity < fail_threshold or body_similarity < fail_threshold:
                    exit_code = ReturnCode.THRESHOLD_EXCEEDED
                    break

        self.compute_overall_score(code_similarity)
        return (exit_code, code_similarity)

    def printer(self, result):
        exit_code, code_similarity = result
        for file1, similarities in code_similarity.items():
            print(f"\nSimilarity for {file1}:")
            for file2, (name_similarity, body_similarity) in similarities.items():
                name_level = self.compute_similarity_level(name_similarity)
                body_level = self.compute_similarity_level(body_similarity)
                print(
                    f"- {file2}: Name similarity: {name_similarity:.2f} ({name_level}), Body similarity: {body_similarity:.2f} ({body_level})")
        print(f"\nOverall Score: {self.overall_score:.2f}")
        print(f"Exit code: {exit_code.value}")

    def main(self):
        parser = argparse.ArgumentParser(description="Duplicate code finder")
        parser.add_argument(
            "-t",
            "--fail-threshold",
            type=float,
            default=0.8,
            help="The minimum required score before the script exits with an error."
        )
        parser.add_argument(
            "-d",
            "--directories",
            nargs='+',
            help="Check for similarities between all files in the specified directories."
        )
        args = parser.parse_args()
        result = self.run(args.fail_threshold, args.directories)
        self.printer(result)
        return result


if __name__ == "__main__":
    finder = DuplicationFinder()
    exit_code, _ = finder.main()
    sys.exit(exit_code.value)
