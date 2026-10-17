from app.seed_data import seed_initial_documents
from app.rag.retriever import retrieve_context
from app.rag.answer_generator import generate_answer

def main():
    # Step 1: Seed of initial documents
    seed_initial_documents()

    # Step 2: Ask questions until the user quits
    while True:
        try:
            question = input("\nWrite your question (or 'quit'): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            return

        if question.lower() == "quit":
            print("Goodbye!")
            return

        if not question:
            print("You should write a question.")
            continue

        documents = retrieve_context(question=question, top_k=1)

        if not documents:
            print("No context was found in the collection.")
            continue
        print("Documents retrieved!")

        answer = generate_answer(
            question=question,
            retrieved_documents=documents,
        )

        print(f"\nChatbot: {answer}\n")


if __name__ == "__main__":
    main()
