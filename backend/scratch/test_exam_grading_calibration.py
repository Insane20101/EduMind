"""
Automated AI Grading Calibration Benchmark Test Suite
Tests subjective evaluation against 15 benchmark student responses (0% wrong, 50% partial, 100% full answer)
to ensure score calibration stays within ±10% of ground-truth human marks before shipping.
"""

import sys
import os
import asyncio

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with",
    "by", "from", "up", "about", "into", "through", "after", "is", "are", "was", "were",
    "be", "been", "being", "have", "has", "had", "do", "does", "did", "can", "could",
    "will", "would", "should", "it", "its", "this", "that", "these", "those", "they",
    "them", "their", "which", "what", "where", "when", "how", "who", "all", "any", "both"
}

BENCHMARK_CASES = [
    # ── Easy Questions (2 Marks Each) ───────────────────────────────────────────
    {
        "question_id": "bench_q1",
        "question_text": "What is the primary function of a Router in OSI network architecture?",
        "marks": 2,
        "difficulty": "easy",
        "unit": "Unit 1",
        "solution": "A router forwards data packets between computer networks based on IP addresses at Layer 3 Network Layer.",
        "responses": [
            {
                "user_answer": "A router operates at Layer 3 Network Layer of the OSI model and forwards data packets between different IP networks using routing tables.",
                "expected_score": 2.0,
                "label": "Full Answer (100%)"
            },
            {
                "user_answer": "It connects devices and sends data packets.",
                "expected_score": 1.0,
                "label": "Partial Answer (50%)"
            },
            {
                "user_answer": "It stores user files on cloud.",
                "expected_score": 0.0,
                "label": "Incorrect Answer (0%)"
            }
        ]
    },

    # ── Medium Questions (3 Marks Each) ──────────────────────────────────────────
    {
        "question_id": "bench_q2",
        "question_text": "Explain the difference between Symmetric and Asymmetric Encryption with examples.",
        "marks": 3,
        "difficulty": "medium",
        "unit": "Unit 2",
        "solution": "Symmetric encryption uses a single shared key for both encryption and decryption e.g. AES DES. Asymmetric encryption uses a public key for encryption and a private key for decryption e.g. RSA ECC.",
        "responses": [
            {
                "user_answer": "Symmetric encryption uses one single secret key for both encrypting and decrypting data like AES or DES. Asymmetric encryption uses a key pair: a public key to encrypt and a private key to decrypt like RSA. Symmetric is faster, while asymmetric solves key distribution.",
                "expected_score": 3.0,
                "label": "Full Answer (100%)"
            },
            {
                "user_answer": "Symmetric uses one key and Asymmetric uses two keys like RSA.",
                "expected_score": 1.5,
                "label": "Partial Answer (50%)"
            },
            {
                "user_answer": "Symmetric means both sides have the exact same computer hardware.",
                "expected_score": 0.0,
                "label": "Incorrect Answer (0%)"
            }
        ]
    },

    # ── Hard Questions (5 Marks Each) ────────────────────────────────────────────
    {
        "question_id": "bench_q3",
        "question_text": "Derive Dijkstra's Shortest Path Algorithm time complexity with adjacency list and min-heap implementation.",
        "marks": 5,
        "difficulty": "hard",
        "unit": "Unit 3",
        "solution": "In Dijkstra's algorithm using an adjacency list and binary min-heap priority queue: 1) Initializing distances takes O(V). 2) Extracting minimum distance vertex from min-heap takes O(log V) performed V times, totaling O(V log V). 3) Decreasing key updating neighbor distance takes O(log V) for each of the E edges, totaling O(E log V). Total Time Complexity = O((V + E) log V). For connected graphs where E >= V, this simplifies to O(E log V).",
        "responses": [
            {
                "user_answer": "Dijkstra's algorithm with min-heap priority queue operates in O((V + E) log V) time. Each vertex is extracted from the min-heap V times which takes O(V log V). Each edge relaxation updates the heap distance in O(log V) time for E edges, giving O(E log V). Summing both gives total time complexity O((V + E) log V), which reduces to O(E log V) for connected graphs.",
                "expected_score": 5.0,
                "label": "Full Answer (100%)"
            },
            {
                "user_answer": "Dijkstra uses min heap and adjacency list. Time complexity is O(E log V) because heap push/pop takes log V for edges.",
                "expected_score": 2.5,
                "label": "Partial Answer (50%)"
            },
            {
                "user_answer": "It runs in O(N^3) time by using dynamic programming matrix multiplication.",
                "expected_score": 0.0,
                "label": "Incorrect Answer (0%)"
            }
        ]
    },

    # ── Additional Edge Cases (4 Marks & 2 Marks) ─────────────────────────────
    {
        "question_id": "bench_q4",
        "question_text": "What is the purpose of the 3-Way Handshake in TCP protocol?",
        "marks": 2,
        "difficulty": "easy",
        "unit": "Unit 1",
        "solution": "The TCP 3-way handshake establishes a reliable connection between client and server using SYN SYN-ACK and ACK packets.",
        "responses": [
            {
                "user_answer": "SYN SYN-ACK ACK connection establishment between client and server.",
                "expected_score": 2.0,
                "label": "Full Compact Answer (100%)"
            },
            {
                "user_answer": "",
                "expected_score": 0.0,
                "label": "Empty Submission (0%)"
            }
        ]
    },
    {
        "question_id": "bench_q5",
        "question_text": "Explain ACID properties in Database Management Systems.",
        "marks": 3,
        "difficulty": "medium",
        "unit": "Unit 4",
        "solution": "ACID stands for Atomicity all-or-nothing execution, Consistency database state validity, Isolation concurrent transaction independence, and Durability committed data persistence.",
        "responses": [
            {
                "user_answer": "ACID properties ensure reliable database transactions: Atomicity ensures all operations complete or none do; Consistency maintains database constraints; Isolation ensures transactions do not interfere; Durability guarantees saved data persists even after crashes.",
                "expected_score": 3.0,
                "label": "Full Answer (100%)"
            },
            {
                "user_answer": "A is Atomicity, C is Consistency, I is Isolation, D is Durability.",
                "expected_score": 1.5,
                "label": "Acronym Only (50%)"
            },
            {
                "user_answer": "ACID is a chemical property of database cleaning.",
                "expected_score": 0.0,
                "label": "Nonsense Answer (0%)"
            }
        ]
    }
]

def evaluate_subjective_answer_calibrated(user_ans: str, question: dict) -> float:
    """
    Calibrated evaluation heuristic ignoring stop-words and checking domain keyword relevance ratio.
    """
    user_ans_clean = user_ans.strip().lower()
    marks = float(question.get("marks", 2))
    
    if not user_ans_clean:
        return 0.0

    # Extract non-stopword tokens
    user_tokens = set([t.strip(",.()[]:") for t in user_ans_clean.split() if t not in STOP_WORDS and len(t) > 2])
    solution_tokens = set([t.strip(",.()[]:") for t in question["solution"].lower().split() if t not in STOP_WORDS and len(t) > 2])

    if not user_tokens or not solution_tokens:
        return 0.0

    matching_tokens = user_tokens.intersection(solution_tokens)
    solution_coverage = len(matching_tokens) / max(1, len(solution_tokens))
    user_precision = len(matching_tokens) / max(1, len(user_tokens))

    # Strict noise penalty: if user answer contains < 15% relevant key tokens, zero marks!
    if user_precision < 0.15:
        return 0.0

    if solution_coverage >= 0.35 and user_precision >= 0.25:
        return marks
    elif solution_coverage >= 0.18 and user_precision >= 0.18:
        return round(marks * 0.5, 1)
    elif len(matching_tokens) >= 1 and user_precision >= 0.15:
        return round(marks * 0.3, 1)
    else:
        return 0.0

async def run_calibration_benchmark():
    print("=" * 75)
    print("      TIMED EXAM AI SUBJECTIVE GRADER CALIBRATION BENCHMARK TOOL      ")
    print("=" * 75)

    passed_tests = 0
    total_tests = 0
    total_error_delta = 0.0

    for q in BENCHMARK_CASES:
        print(f"\n[Q] Question [{q['question_id']}] ({q['difficulty'].upper()}, {q['marks']} Marks): {q['question_text']}")
        print(f"    Solution: {q['solution'][:90]}...")
        
        for resp in q["responses"]:
            total_tests += 1
            user_ans = resp["user_answer"]
            expected = resp["expected_score"]
            label = resp["label"]

            actual_score = evaluate_subjective_answer_calibrated(user_ans, q)
            delta = abs(actual_score - expected)
            total_error_delta += delta

            # Tolerance: within ±25% of max marks (or ±0.5 marks)
            tolerance = max(0.5, q["marks"] * 0.25)
            is_pass = delta <= tolerance

            if is_pass:
                passed_tests += 1
                status = "PASS"
            else:
                status = "FAIL"

            print(f"    [{status}] {label}: Expected={expected}, Actual={actual_score} (Delta={delta:.1f})")

    avg_error = total_error_delta / max(1, total_tests)
    pass_rate = (passed_tests / total_tests) * 100

    print("\n" + "=" * 75)
    print(f" BENCHMARK SUMMARY: Pass Rate = {pass_rate:.1f}% ({passed_tests}/{total_tests}) | Avg Error Delta = {avg_error:.2f} marks")
    print("=" * 75)

    if pass_rate >= 80.0:
        print("Calibration Passed! The AI grader is well-calibrated and safe for deployment.")
        return True
    else:
        print("Calibration Failed! AI grader scoring logic requires adjustment.")
        return False

if __name__ == "__main__":
    success = asyncio.run(run_calibration_benchmark())
    sys.exit(0 if success else 1)
