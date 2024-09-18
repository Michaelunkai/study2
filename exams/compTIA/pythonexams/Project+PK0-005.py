def main():
    questions_answers = [
        {
            "question": "\033[1mQuestion 1\033[0m\nBefore the final product is launched, the marketing team suggests presenting the product to a predefined set of customers who may be able to provide relevant insight for improvement. Which of the following would the project manager MOST likely conduct?\nA. Workshop\nB. Brainstorming\nC. Stand-up\nD. Focus group",
            "answer": "D"
        },
        {
            "question": "\033[1mQuestion 2\033[0m\nWhich of the following would be the MOST important consideration for call center personnel accepting customer orders and payments on a website?\nA. Intellectual property protection\nB. Branding restrictions\nC. Personally identifiable information security\nD. Multifactor authentication",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 3\033[0m\nA project manager is performing the initial risk assessment on a risk that has been highlighted. Which of the following steps should be executed as part of this assessment?\nA. Identifying project communication methods\nB. Determining the impact of risks\nC. Rewriting the scope of work\nD. Defining key project resources",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 4\033[0m\nA project manager experiences issues that may delay the project from moving toward production release due to the stakeholder's refusal to sign off. The stakeholder thinks this step should be done by someone else. Which of the following should the project manager review?\nA. RBS\nB. RACI\nC. WBS\nD. CCB",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 5\033[0m\nA project manager has been assigned to a new project and is informed that a similar issue was resolved on another project last year. Which of the following should the project manager do NEXT?\nA. Determine the solution design.\nB. Review existing artifacts.\nC. Define the preliminary scope statement.\nD. Identify the stakeholders.",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 6\033[0m\nIn the kickoff meeting, a project manager announced the project will use a tool to store documents, artifacts, and any other data relevant to the project. The tool will perform version control, maintain retention data, and archive destruction or historical information. Which of the following is being described?\nA. Record management system\nB. Project dashboard\nC. Backlog\nD. Wiki knowledge base",
            "answer": "A"
        },
        {
            "question": "\033[1mQuestion 7\033[0m\nA project manager prepared a project closeout report for stakeholders, clients, and team members. Which of the following describes the benefits of the project closeout report?\nA. It highlights team members who underperformed.\nB. It allows the project manager to explain and justify poor outcomes.\nC. It shows the project manager's perspective on the project.\nD. It helps the project manager to determine what worked well and what can be improved.",
            "answer": "D"
        },
        {
            "question": "\033[1mQuestion 8\033[0m\nThe PMO has just reduced a project's priority from 4 to 12 out of 22. As a result of the project prioritization change, the highly skilled resources have been reassigned to higher priority projects. The issue has been recorded on the issue log, and the change in resources has been included on the change control log. Which of the following should the project manager do NEXT?\nA. Inform the project team that mandatory overtime is required for the remainder of the project.\nB. Conduct an impact assessment to determine the effects on the project baselines.\nC. Encourage the project sponsor to use referent power to get the project's priority elevated.\nD. Accept the change and cite the resource reduction whenever there is a schedule slippage.",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 9\033[0m\nA project manager wants to know the billable hours an employee has spent on a project. Which of the following can the project manager use?\nA. Project status report\nB. Calendaring tools\nC. Time-tracking tools\nD. Task board",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 10\033[0m\nA risk that equipment may be delayed develops during a project. The project team is experiencing:\nA. scope creep.\nB. a change.\nC. an issue.\nD. a work-around.",
            "answer": "C"
        }
    ]

    score = 0

    for qa in questions_answers:
        print(qa["question"])
        user_answer = input("Your answer (A/B/C/D): ").strip().upper()
        correct_answer = qa["answer"]

        if user_answer == correct_answer:
            print("Correct!\n")
            score += 1
        else:
            print(f"Incorrect. The correct answer is {correct_answer}.\n")

    print("Your final score:", score, "out of", len(questions_answers))

if __name__ == "__main__":
    main()
