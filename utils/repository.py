import os
import json
from git.repo import Repo
from git.repo.fun import is_git_dir


class GitRepository(object):
    """
    git仓库管理
    """

    def __init__(self, local_path, repo_url, branch='master'):
        """
        :param local_path: 本地git项目的值
        :param repo_url: git仓库地址，https://www.xxxxx.git
        :param branch:
        """
        self.local_path = local_path
        self.repo_url = repo_url
        self.repo = None
        self.initial(branch)

    def initial(self, branch):
        """
        初始化git仓库
        :param repo_url:
        :param branch:
        :return:
        """
        if not os.path.exists(self.local_path):
            os.makedirs(self.local_path)
        git_local_path = os.path.join(self.local_path, '.git')

        if not is_git_dir(git_local_path):
            self.repo = Repo.clone_from(self.repo_url, to_path=self.local_path, branch=branch)
        else:
            self.repo = Repo(self.local_path)

    def pull(self):
        """
        从线上拉最新代码
        :return:
        """
        self.repo.git.pull()

    def branches(self):
        """
        获取所有分支
        :return:
        """
        branches = self.repo.remote().refs
        return [item.remote_head for item in branches if item.remote_head not in ['HEAD', ]]

    def commits(self, max_count=50):
        """
        获取所有提交记录
        :return:
        """
        commit_log = self.repo.git.log('--pretty={"commit":"%h","author":"%an","summary":"%s","date":"%cd"}',
                                       max_count=max_count,
                                       date='format:%Y-%m-%d %H:%M')
        return [json.loads(item) for item in commit_log.split('\n')]

    def tags(self):
        """
        获取所有tag
        :return:
        """
        return [tag.name for tag in self.repo.tags]

    def change_to_branch(self, branch):
        """
        切换分值
        :param branch:
        :return:
        """
        self.repo.git.checkout(branch)

    def change_to_commit(self, branch, commit):
        """
        切换commit
        :param branch:
        :param commit:
        :return:
        """
        self.change_to_branch(branch=branch)
        self.repo.git.reset('--hard', commit)

    def change_to_tag(self, tag):
        """
        切换tag
        :param tag:
        :return:
        """
        self.repo.git.checkout(tag)


if __name__ == '__main__':
    local_path = os.path.join('codes', 'luffycity')
    repo_object = GitRepository(local_path, 'https://gitee.com/wupeiqi/xxoo.git')

    # 本地暂存代码
    index = repo_object.repo.index
    index.add(['new.txt'])
    index.commit('this is a test')
    # 提交到远程
    remote = repo_object.repo.remote()
    remote.push()



