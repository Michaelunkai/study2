from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # Replace this list with your skills
    skills = ["Virtualization (hosted+bare metal. VMware, oracle, hyperV, QEMU, sandbox, proxmox)", "Docker( deploying, networking, optimization, troubleshooting) ", "Linux(All Distros, networking, optimization, bash&scripting, automation, security, services, monitoring, administration, managment)", "Backing up(planning and strategy, automation, Data Deduplication and Compression, testing, disaster backup and recovery) ","skill 5", "skill 6", "skill 7"]
    return render_template('index.html', skills=skills)

if __name__ == '__main__':
    app.run(debug=True)
