import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class SysAdminExamApp extends JFrame {
    private static final int TOTAL_QUESTIONS = 10;
    private String[] questions = {
        "1. Which command shows all active network connections?",
        "2. How do you check disk usage in a human-readable format?",
        "3. Which command is used to check memory usage?",
        "4. How do you list all running processes?",
        "5. Which command is used to change file permissions?",
        "6. How do you display the current directory?",
        "7. Which command is used to search for a pattern in files?",
        "8. How do you install a package using apt?",
        "9. How do you restart the network service?",
        "10. Which command is used to view system logs?"
    };

    private String[][] options = {
        {"a) netstat", "b) ifconfig", "c) ping"},
        {"a) df -h", "b) du -h", "c) ls -lh"},
        {"a) free -m", "b) top", "c) vmstat"},
        {"a) ps aux", "b) top", "c) htop"},
        {"a) chmod", "b) chown", "c) chgrp"},
        {"a) pwd", "b) cd", "c) ls"},
        {"a) grep", "b) find", "c) awk"},
        {"a) apt-get install", "b) apt install", "c) installpkg"},
        {"a) systemctl restart networking", "b) service network restart", "c) /etc/init.d/networking restart"},
        {"a) tail /var/log/syslog", "b) cat /var/log/messages", "c) journalctl"}
    };

    private String[] hints = {
        "Hint: Think about a command that lists network interfaces and routes.",
        "Hint: It's a disk space checking command.",
        "Hint: It's a command that shows free and used memory.",
        "Hint: It's a command that lists all the processes running on the system.",
        "Hint: It's a command used to modify file access rights.",
        "Hint: It's a command that prints the working directory.",
        "Hint: It's a command that matches patterns in files.",
        "Hint: It's a package management command.",
        "Hint: It's a command used to manage system services.",
        "Hint: It's a command used to view logs in the system."
    };

    private String[] answers = {
        "a", "b", "a", "a", "a", "a", "a", "b", "a", "c"
    };

    private JComboBox<String>[] comboBoxes = new JComboBox[TOTAL_QUESTIONS];
    private JButton[] hintButtons = new JButton[TOTAL_QUESTIONS];
    private JButton[] answerButtons = new JButton[TOTAL_QUESTIONS];
    private JLabel[] hintLabels = new JLabel[TOTAL_QUESTIONS];
    private JLabel[] answerLabels = new JLabel[TOTAL_QUESTIONS];

    public SysAdminExamApp() {
        setTitle("Sys Admin Exam App");
        setSize(800, 600);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new GridBagLayout());
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.fill = GridBagConstraints.HORIZONTAL;
        gbc.insets = new Insets(5, 5, 5, 5);

        for (int i = 0; i < TOTAL_QUESTIONS; i++) {
            gbc.gridx = 0;
            gbc.gridy = i;
            gbc.gridwidth = 2;
            add(new JLabel(questions[i]), gbc);

            gbc.gridx = 2;
            gbc.gridy = i;
            gbc.gridwidth = 1;
            comboBoxes[i] = new JComboBox<>(options[i]);
            add(comboBoxes[i], gbc);

            hintButtons[i] = new JButton("Hint");
            gbc.gridx = 3;
            hintButtons[i].addActionListener(new HintButtonActionListener(i));
            add(hintButtons[i], gbc);

            hintLabels[i] = new JLabel("");
            gbc.gridx = 4;
            add(hintLabels[i], gbc);

            answerButtons[i] = new JButton("Answer");
            gbc.gridx = 5;
            answerButtons[i].addActionListener(new AnswerButtonActionListener(i));
            add(answerButtons[i], gbc);

            answerLabels[i] = new JLabel("");
            gbc.gridx = 6;
            add(answerLabels[i], gbc);
        }

        JButton finishButton = new JButton("Finish & Test");
        finishButton.addActionListener(new FinishButtonActionListener());
        gbc.gridx = 0;
        gbc.gridy = TOTAL_QUESTIONS;
        gbc.gridwidth = 7;
        add(finishButton, gbc);

        setVisible(true);
    }

    private class HintButtonActionListener implements ActionListener {
        private int index;

        public HintButtonActionListener(int index) {
            this.index = index;
        }

        @Override
        public void actionPerformed(ActionEvent e) {
            hintLabels[index].setText(hints[index]);
        }
    }

    private class AnswerButtonActionListener implements ActionListener {
        private int index;

        public AnswerButtonActionListener(int index) {
            this.index = index;
        }

        @Override
        public void actionPerformed(ActionEvent e) {
            answerLabels[index].setText("Correct Answer: " + answers[index]);
        }
    }

    private class FinishButtonActionListener implements ActionListener {
        @Override
        public void actionPerformed(ActionEvent e) {
            int score = 0;
            for (int i = 0; i < TOTAL_QUESTIONS; i++) {
                if (comboBoxes[i].getSelectedItem().toString().charAt(0) == answers[i].charAt(0)) {
                    score += 10;
                }
            }
            JOptionPane.showMessageDialog(null, "Your score is: " + score + "/100");
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            @Override
            public void run() {
                new SysAdminExamApp();
            }
        });
    }
}
