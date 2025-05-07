import json
import itertools
import os
import argparse

def load_data(filename):
    """Load the dataset from a JSON file."""
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def save_results(results, output_filename):
    """Save the comparison results to a JSON file."""
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Results saved to {output_filename}")

# def run_comparisons(data):
#     """Run pairwise comparisons for each prompt and its answers."""
#     results = []
#     idx = 1
#     for item in data:
#         os.system('cls')
#         prompt = item["prompt"]
#         answers = item["answers"]
        
#         print("\n" + "="*50)
#         print(f"PROMPT: {prompt}")
#         print("="*50 + "\n")
        
#         # Generate all possible pairs of answers (combinations of 2)
#         answer_pairs = list(itertools.combinations(range(len(answers)), 2))
#         total_comparisons = len(answer_pairs)
        
#         print(f"Total comparisons to make: {total_comparisons}")
        
#         for i, (idx_a, idx_b) in enumerate(answer_pairs):
#             print(f"\nCOMPARISON {i+1}/{total_comparisons}:")
#             print(f"-- Option 1:\n{answers[idx_a]['content']}\n")
#             print(f"-- Option 2:\n{answers[idx_b]['content']}\n")
            
#             while True:
#                 choice = input("Enter 1 for Option 1 or 2 for Option 2: ")
#                 if choice in ['1', '2']:
#                     break
#                 print("Invalid input. Please enter 1 or 2.")
            
#             accepted_idx = idx_a if choice == '1' else idx_b
#             rejected_idx = idx_b if choice == '1' else idx_a
            
#             results.append({
#                 "prompt": prompt,
#                 "accepted": answers[accepted_idx]["content"],
#                 "rejected": answers[rejected_idx]["content"],
#                 "uid": idx
#             })
#         idx+=1
    
#     return results
def run_comparisons(data):
    """For each prompt, ask for a ranking string and generate all pairwise comparisons."""
    results = []
    for uid, item in enumerate(data, start=1):
        prompt = item["prompt"]
        answers = item["answers"]
        n = len(answers)

        # Display prompt and options
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" + "="*50)
        print(f"PROMPT #{uid + 26}: {prompt}")
        print("="*50 + "\n")
        for i, ans in enumerate(answers, start=1):
            print(f"[{i}] {ans['content']}\n")

        # Get and validate ranking input
        
        while True:
            example = "".join(str(i) for i in range(n, 0, -1))
            ranking = input(f"Enter a {n}-digit ranking (best→worst), e.g. '{example}': ").strip()
            if len(ranking) != n or not ranking.isdigit():
                print(f"↳ Invalid: must be exactly {n} digits, each from 1 to {n}.")
                continue
            ranks = [int(d) for d in ranking]
            if sorted(ranks) != list(range(1, n+1)):
                print(f"↳ Invalid: digits must be a permutation of 1..{n}.")
                continue
            break

        # Build a map: answer_index (0-based) -> rank position (0 is best)
        rank_map = {ans_idx: position
                    for position, ans_idx in enumerate([d-1 for d in ranks])}

        # Generate all pairwise comparisons
        for idx_a, idx_b in itertools.combinations(range(n), 2):
            if rank_map[idx_a] < rank_map[idx_b]:
                accepted_idx, rejected_idx = idx_a, idx_b
            else:
                accepted_idx, rejected_idx = idx_b, idx_a

            results.append({
                "prompt": prompt,
                "accepted": answers[accepted_idx]["content"],
                "rejected": answers[rejected_idx]["content"],
                "uid": (uid + 26)
            })

    return results

def main():
    parser = argparse.ArgumentParser(description="Process dataset paths for reward comparison.")
    parser.add_argument("--input", type=str, required=True, help="Path to the input dataset file")
    parser.add_argument("--output", type=str, required=True, help="Path to save the final results")
    
    args = parser.parse_args()
    
    input_file = args.input
    output_file = args.output

    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        return
            
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        return
    
    try:
        data = load_data(input_file)
        print(f"Successfully loaded data with {len(data)} prompts.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON file.")
        return
    except Exception as e:
        print(f"Error loading file: {e}")
        return
    
    results = run_comparisons(data)
    
    save_results(results, output_file)
    
    total_comparisons = len(results)
    unique_prompts = len(set(item["prompt"] for item in results))
    print(f"\nSummary: Completed {total_comparisons} comparisons across {unique_prompts} unique prompts.")

if __name__ == "__main__":
    main()