
def main():
    print("Welcome to the Exam!")

    questions_answers = [
        {
            "question": "\033[1mQuestion 1\033[0m\nAn instructor demonstrates effective communication skills when doing all of the following EXCEPT:\nA. using technical terms familiar to the learners\nB. rephrasing and restating key terms until the learners understand the message\nC. using terminology that emphasizes the instructor's intelligence and credibility\nD. using frames of reference that are familiar to the learners",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 2\033[0m\nWhich of the following is the most appropriate response by an instructor to a learner-generated question that clearly indicates confusion about the course content?\nA. Responding immediately to learners with the correct answer\nB. Reviewing the basic concepts with the entire class\nC. Explaining that the learner's question is answered in the course materials\nD. Rephrasing the learner's question to determine the source of the confusion",
            "answer": "D"
        },
        {
            "question": "\033[1mQuestion 3\033[0m\nAn instructor is preparing to teach a class and notices that the instructor guide does not offer students any way to check their learning. In this situation, the instructor should:\nA. develop questions to give the students during the teaching of the class\nB. create a take-home test to give the students at the end of the class\nC. have the class create questions to use as a self-study guide\nD. expect the learners to determine how well they understand the material",
            "answer": "A"
        },
        {
            "question": "\033[1mQuestion 4\033[0m\nDuring a class, it is clear students have little understanding of the information. Students are becoming less and less interested in attempting to answer questions the trainer is asking during the course of instruction. In this situation, the trainer should:\nA. stop asking questions for a period of time\nB. change the way of responding to students' answers\nC. address yes-no questions to the full class\nD. provide the answers quickly, avoiding silences",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 5\033[0m\nAn instructor is teaching a five-day, advanced-level course for experienced users of a specific software program. The participants' supervisor determined who should attend the course. On the morning of the first day, as the group of participants were arriving, one of the learners expressed surprise to have been included in the class. The learner had spent much less time using the software than the others in the class. This situation best supports which of the following conclusions?\nA. An instructor should talk with all learners prior to the start of the course to ensure that all learners' concerns are addressed ahead of time.\nB. An instructor should be able to plan and adjust instruction to account for learner differences during the course.\nC. An instructor should allow time at the beginning of a course for administering a short pretest on the course content.\nD. An instructor should formally survey learners before the course begins to avoid potential problems that could delay the session.",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 6\033[0m\nFor this question, decide whether the action makes it likely or unlikely that the trainer will achieve the goal. Select the best statement of the reason that the action is likely or unlikely to accomplish the goal.\nGoal: To lead beginner-level learners to a thorough understanding of a concept that has just been presented to them.\nAction: Frame systematic questions in a way that requires the learners first to apply the concept and then to recall facts regarding the concept.\nA. Likely, because the learners will have the benefit of guidance from the instructor\nB. Likely, because the questioning technique will enable learner success and confidence\nC. Unlikely, because the instructor is requiring learners to begin by responding to a cognitively higher-level question\nD. Unlikely, because planned systematic questioning rarely aids learning",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 7\033[0m\nFor this question, decide whether the action makes it likely or unlikely that the trainer will achieve the goal. Select the best statement of the reason that the action is likely or unlikely to accomplish the goal.\nGoal: To provide motivational feedback to a group of learners who are having difficulty applying a skill they have been taught and feeling insecure about their ability to meet the course objectives.\nAction: The instructor has the group of learners stay after each class session and provides each with a confidential written evaluation of their performance in the session.\nA. Likely, because the group of learners will appreciate the instructor's extra concern\nB. Likely, because the learners will appreciate that the reports are confidential\nC. Unlikely, because the instructor has established a positive learning environment\nD. Unlikely, because the group of learners will experience increased anxiety",
            "answer": "D"
        },
        {
            "question": "\033[1mQuestion 8\033[0m\nTwo instructors are team-teaching a course designed to be delivered by two instructors. Test results show that learners consistently perform better whenever this material is presented by one of the instructors. The first response to this situation should be to:\nA. involve the learners' employers in the evaluation process\nB. evaluate the effect on learner performance of each instructor's style\nC. administer a final exam sampling all materials taught in the course\nD. assign the course to two more experienced instructors",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 9\033[0m\nFor this question, decide whether the action makes it likely or unlikely that the trainer will achieve the goal. Select the best statement of the reason that the action is likely or unlikely to accomplish the goal.\nGoal: To respond appropriately to learner needs for clarification and feedback\nAction: After explaining a key point, the instructor asks the class if they have any questions.\nA. Likely, because if the learners have questions about the key point, they will ask questions\nB. Likely, because encouraging responses facilitates learning\nC. Unlikely, because learners are often unwilling to indicate a lack of understanding\nD. Unlikely, because the instructor has failed to consider nonverbal cues",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 10\033[0m\nFor this question, decide whether the action makes it likely or unlikely that the instructor will achieve the goal. Select the best statement of the reason that the action is likely or unlikely to accomplish the goal.\nGoal: To train a group of machine operators to use a new piece of equipment\nAction: The instructor modifies a course designed for self-taught learning and lectures it instead.\nA. Likely, because all learning objectives will be covered in the material\nB. Likely, because the instructor can elaborate on material covered in the course\nC. Unlikely, because individual learning objectives are different from group learning objectives\nD. Unlikely, because lecturing is less effective for learning hands-on skills",
            "answer": "D"
        },
        {
            "question": "\033[1mQuestion 11\033[0m\nAn instructor is teaching a course where the learners are required to be accredited through a third party certification body. The instructor prepares the class and then creates a difficult final exam. Which of the following would be the BEST reason for doing this?\nA. To encourage the learners to work harder in the class\nB. To over-prepare the learners so the exam will seem easy\nC. To ensure the learners' success with the third party exam\nD. To place additional stress on the importance of the material",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 12\033[0m\nAn instructor wants to be available to the learners after the completion of the course but does not want to reveal any personal information. Which of the following might be the BEST method for post-course support?\nA. The website of the instructor\nB. Distribute the instructor’s email address\nC. Independent website discussion forum\nD. Contact through the hosting facility",
            "answer": "D"
        },
        {
            "question": "\033[1mQuestion 13\033[0m\nAt the end of a course an instructor needs to verify that the learning objectives are met by learned:\nA. assignments\nB. knowledge\nC. abilities\nD. achievements",
            "answer": "D"
        },
        {
            "question": "\033[1mQuestion 14\033[0m\nDuring a course it is found that the material does not properly reflect the needs of the learners. The course is scheduled to be offered several times over the next three months within the same organization that would like the course more tailored. Which of the following is MOST likely to achieve this desired result?\nA. post-course review\nB. Changing the instructor\nC. A learner selection that matches the course outline better\nD. Using a different vendor of course material",
            "answer": "A"
        },
        {
            "question": "\033[1mQuestion 15\033[0m\nWhen writing a review of learners in a training course, the instructor inadvertently misidentifies a learner and comments negatively on their participation and competency of the material in their written report. Which of the following is the MOST serious repercussion to the instructor?\nA. Could be sued for defamation\nB. Could forfeit pay\nC. Would most likely not be asked to teach future classes\nD. No repercussion could happen as this is considered routine error",
            "answer": "A"
        },
        {
            "question": "\033[1mQuestion 16\033[0m\nDuring introductions a learner asks if a related topic can be reviewed during the course; however, the topic is outside the prescribed course material. Which of the following is the BEST way to handle this request?\nA. Review the topic in the next more advanced course.\nB. Extend the length of the course to include the topic.\nC. Remove a section from the course material to make room for the requested topic.\nD. Include the topic without modifying the course material.",
            "answer": "D"
        },
        {
            "question": "\033[1mQuestion 17\033[0m\nOn the first day of a software training course, the instructor discovers that two of the computers do not have the proper software loaded. Which of the following BEST describes what the instructor could have done to ensure all systems were operational?\nA. Ask the learners to load the machines once they come in.\nB. Inform the customer that all systems need to be loaded before the course begins.\nC. The day of the course load all the systems from the instructor’s software disk to ensure all systems are functional.\nD. Come in the day prior to make sure that all the systems were properly loaded.",
            "answer": "D"
        },
        {
            "question": "\033[1mQuestion 18\033[0m\nWhile delivering training, several learners are making fun of another instructor’s shortcomings from a pre-requisite course. Which of the following is the BEST way to handle this situation?\nA. Correct the learners in front of the class.\nB. Continue with the course.\nC. Agree with the learner’s comments.\nD. State that the classroom is not the place for these types of conversation.",
            "answer": "D"
        },
        {
            "question": "\033[1mQuestion 19\033[0m\nDuring discussion a learner challenges an answer the instructor provides. Which of the following is the BEST method for handling the situation?\nA. The instructor should answer the questions to demonstrate product knowledge and transfer information.\nB. Always make the supporting documentation the authority when answering questions.\nC. Poll the learners for best practices and to develop a frame of reference for the question.\nD. Create a classroom discussion with learners enabling them to learn from each other.",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 20\033[0m\nAt the beginning of a training session dealing with very large equipment, an instructor observes that some learners seem nervous. During introductions the same learners indicate they are unsure of their ability to learn such a large piece of equipment. Which of the following is the instructor’s BEST action?\nA. Advise the learners to take the class at their own pace and then assign groups so not all learners will have to deal with the large equipment.\nB. Inform the learners that the training is a job requirement that everyone must complete.\nC. Advise the learners of the course objectives, timeline, and define requirements for passing the course.\nD. Encourage the learners and compare their skills to the training objectives and current job requirements.",
            "answer": "D"
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
