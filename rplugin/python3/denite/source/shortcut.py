# ============================================================================
# FILE: shortcut.py
# ============================================================================

from os import path

from denite.base.source import Base
from denite.kind.command import Kind as Command

from denite.util import globruntime, Nvim, UserContext, Candidates


class Source(Base):

    def __init__(self, vim: Nvim) -> None:
        super().__init__(vim)

        self.name = 'shortcut'
        self.kind = Kind(vim)

    def gather_candidates(self, context: UserContext) -> Candidates:
        shortcuts = {}

        for shortcut, description in self.vim.vars["shortcuts"].items():
            if self.vim.vars['shortcut_expand_leader_keys'] == 1:
                shortcut = self.vim.eval(f'ShortcutLeaderKeys("{shortcut}")')

            shortcuts[shortcut] = {
                'word': '{0:<12} -- {1}'.format(shortcut, description),
                'action__command': shortcut
            }

        return sorted(shortcuts.values(), key=lambda value: value['word'])


class Kind(Command):

    def __init__(self, vim: Nvim) -> None:
        super().__init__(vim)

        self.name = 'shortcut'

    def action_execute(self, context: UserContext) -> None:
        target = context['targets'][0]
        command = target['action__command']
        self.vim.command(f'call ShortcutFeedKeys("{command}")')

    def action_edit(self, context: UserContext) -> None:
        return super().action_execute(context)
