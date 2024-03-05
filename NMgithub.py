from git import Repo, GitCommandError

GITHUB_USERNAME = 'ravangs'
REPO_NAME = 'netman-lab-midterm'
REPO_PATH = '/home/student/labs/labmidterm'
FILES_TO_PUSH = ['data.txt','cpu_utilization.jpg']
SSH_PRIVATE_KEY_PATH = '/home/student/.ssh/id_ed25519'

def push_files_to_github():
    try:
        repo = Repo(REPO_PATH)
        
        repo.index.add(FILES_TO_PUSH)
        
        changed_files = [item.a_path for item in repo.index.diff(None)]
        
        changed_files += repo.untracked_files
        
        repo.index.add(changed_files)
        
        repo.index.commit("Pushing updated files")
        
        origin = repo.remote(name='origin')

        origin.push(env={'GIT_SSH_COMMAND': f'ssh -i {SSH_PRIVATE_KEY_PATH}'})

        print('Files pushed to GitHub')
    except GitCommandError as e:
        print(f'Error pushing files to GitHub: {e}')

push_files_to_github()
