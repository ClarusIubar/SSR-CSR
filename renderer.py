import os

class ViewRenderer:
    def __init__(self, base_dir):
        self.template_path = os.path.join(base_dir, 'html')

    def _read(self, name):
        with open(os.path.join(self.template_path, f"{name}.html"), 'r', encoding='utf-8') as f:
            return f.read()

    # SSR은 서버에서 렌더링을 하고서 보여줘야 하니까, 렌더러가 따로 있다.
    def render_index(self, user_data):
        row = self._read('row')
        rows = "".join(row.format(uid=u, task=i['task']) for u, i in user_data.items()) if user_data else self._read('empty')
        return self._read('index').replace('{rows}', rows)

    def render_maslow(self, steps):
        brick = self._read('maslow_brick')
        stack = "".join(brick.format(**step) for step in steps)
        return self._read('maslow').replace('{stack}', stack)