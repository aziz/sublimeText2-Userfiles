import sublime
import sublime_plugin
import os
import re


class PrintThemeRule(sublime_plugin.TextCommand):

    def load_theme(self):
        theme = self.view.settings().get('color_scheme')
        # strip the Packages/
        theme = theme[9:]

        path = os.path.join(sublime.packages_path(), theme)
        with open(path, 'r') as f:
            contents = f.read()

        return contents

    def parse_theme(self, theme):
        return re.findall(r'<key>\s*scope\s*</key>\s*<string>([^<]+)</string>', theme)

    def run(self, edit):
        scope_name = self.view.scope_name(self.view.sel()[0].a)
        selectors = self.parse_theme(self.load_theme())
        best, bestScore = '', 0
        for selector in selectors:
            score = sublime.score_selector(scope_name, selector)
            if score > bestScore:
                bestScore = score
                best = selector

        str = "Selector: |%s| Scope: |%s| Score %d " % (best, scope_name, bestScore)
        print(str)
        sublime.status_message(str)
