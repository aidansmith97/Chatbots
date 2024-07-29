import json
from difflib import get_close_matches
from typing import Optional, List, Dict

def load_kb(file_path: str) -> Dict:
    with open(file_path, 'r') as file:
        data: Dict = json.load(file)
    return data

def save_kb(file_path: str, data: Dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_bm(user_question: str, question: List[str]) -> Optional[str]:
    matches: List[str] = get_close_matches(user_question, question, n=1, cutoff=0.6)
    return matches[0] if matches else None

def gafq(question: str, kb: Dict) -> Optional[str]:
    for q in kb["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None

def chatbot():
    kb: Dict = load_kb('kb.json')

    while True:
        user_input: str = input('You: ')

        if user_input.lower() == "quit":
            break

        best_match: Optional[str] = find_bm(user_input, [q['question'] for q in kb['questions']])

        if best_match:
            answer: Optional[str] = gafq(best_match, kb)
            print(f'Bot: {answer}')
        else:
            print(f'Bot: I do not know the answer, can you teach me please?')
            new_answer: str = input('Type the answer here or "skip" to skip: ')

            if new_answer.lower() != 'skip':
                kb['questions'].append({"question": user_input, "answer": new_answer})
                save_kb('kb.json', kb)
                print("Thank you for helping me learn!")

if __name__ == "__main__":
    chatbot()
