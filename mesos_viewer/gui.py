# -*- coding: utf-8 -*-
import sys
import urwid
import subprocess
import threading

from operator import attrgetter
from datasize import DataSize
from mesos_viewer.popup import Popup
from mesos_viewer.poller import Poller
from mesos_viewer.config import Config
from mesos_viewer import __version__


class ItemWidget(urwid.WidgetWrap):
    """ Widget of listbox, represent each framework """

    def __init__(self, framework, sn=0):
        self.sn = sn
        self.framework = framework
        self.framework_id = framework.id
        self.name = framework.name
        self.url = framework.url
        self.memory = "{:.2GiB}".format(DataSize(framework.memory_str))
        self.cpus = framework.cpus

        self.tasks = framework.tasks
        self.tasks_len = framework.tasks_len
        self.uptime = framework.uptime
        self.uptime_descriptive = framework.uptime_descriptive

        if self.sn is None:
            sn_text = '-'
            sn_align = 'center'
            self.sn = '-'
        else:
            sn_align = 'left'
            sn_text = '%s:' % self.sn

        if self.cpus is None:
            self.cpus = "-"

        if self.memory is None:
            self.memory = "-"

        if int(self.tasks_len) < 1 or int(self.cpus) < 1:
            framework_color = 'bad_name'
        else:
            framework_color = 'name'

        self.item = [
            ('fixed', 4, urwid.Padding(urwid.AttrMap(urwid.Text(sn_text, align=sn_align), framework_color, 'focus'))),
            urwid.AttrMap(urwid.Text(self.name), framework_color, 'focus'),
            ('fixed', 19,
             urwid.Padding(urwid.AttrMap(urwid.Text(self.uptime, align="right"), framework_color, 'focus'))),
            ('fixed', 10,
             urwid.Padding(urwid.AttrMap(urwid.Text(self.memory, align="right"), framework_color, 'focus'))),
            ('fixed', 5,
             urwid.Padding(urwid.AttrMap(urwid.Text(str(self.cpus), align="right"), framework_color, 'focus'))),
            ('fixed', 4,
             urwid.Padding(urwid.AttrMap(urwid.Text(self.tasks_len, align="right"), framework_color, 'focus'))),
            ('fixed', 20, self.get_tasks_str(self.tasks))
        ]

        w = urwid.Columns(self.item, focus_column=1, dividechars=1)
        self.__super.__init__(w)

    def selectable(self):
        return True

    @staticmethod
    def keypress(size, key):
        return key

    @staticmethod
    def to_short_status(status):
        switcher = {
            "TASK_STAGING": get_staging_status(),  # "STG",
            "TASK_STARTING": get_starting_status(),  # "STR",
            "TASK_RUNNING": get_running_status(),  # "RUN",
            "TASK_UNREACHABLE": get_unreachable_status(),  # "URC",
            "TASK_FINISHED": get_finished_status(),  # "FIN",
            "TASK_KILLING": get_killing_status(),  # "KIL",
            "TASK_KILLED": get_killed_status(),  # "KLD",
            "TASK_FAILED": get_failed_status(),  # "FLD"
            "TASK_LOST": get_lost_status()  # "LST"
        }
        return switcher.get(status, urwid.AttrMap(urwid.Text("-", align="right"), 'body', 'focus'))

        # ■ □ ▢ ▣ ▤ ▥ ▦ ▧ ▨ ▩ ▪ ▫ ▬ ▭ ▮ ▯ ▰ ▱ ▲ △ ▴ ▵ ▶ ▷ ▸ ▹ ► ▻ ▼ ▽ ▾ ▿ ◀ ◁ ◂ ◃ ◄ ◅ ◆ ◇ ◈ ◉
        # ◊ ○ ◌ ◍ ◎ ● ◐ ◑ ◒ ◓ ◔ ◕ ◖ ◗ ◘ ◙ ◚ ◛ ◜ ◝ ◞ ◟ ◠ ◡ ◢ ◣ ◤ ◥ ◦ ◧ ◨ ◩ ◪ ◫ ◬ ◭ ◮ ◯ ◰ ◱ ◲ ◳ ●
        # ◴ ◵ ◶ ◷ ◸ ◹ ◺ ◻ ◼ ◽ ◾ ◿

    def get_tasks_str(self, tasks):
        tasks_lst = []
        for task in tasks:
            task_state = self.to_short_status(task["state"])
            tasks_lst.append(task_state)
        return urwid.GridFlow(tasks_lst, 1, 1, 0, 'left')



class MesosGui(object):
    """ The MesosGui object """

    def __init__(self, cache_manager):
        self.cache_manager = cache_manager
        self.already_build = False
        self.on_comments = False
        self.which = "frameworks"
        self.total_frameworks = 0

        self.config = Config()
        self.poller = Poller(
                self, delay=int(
                        self.config.parser.get('settings', 'refresh_interval')))
        self.palette = self.config.get_palette()

        self.sort_on = "name"
        self.sort_reverse = False

        self.sort_asc = "▲"
        self.sort_desc = "▼"
        self.col_name      = "FRAMEWORKS"
        self.col_name_asc  = "FRAMEWORKS▲"
        self.col_name_desc = "FRAMEWORKS▼"
        self.col_memory      = "MEM"
        self.col_memory_asc  = "MEM▲"
        self.col_memory_desc = "MEM▼"
        self.col_cpus      = "CPUs"
        self.col_cpus_asc  = "CPUs▲"
        self.col_cpus_desc = "CPUs▼"
        self.col_uptime     = "UPTIME"
        self.col_uptime_asc  = "UPTIME▲"
        self.col_uptime_desc = "UPTIME▼"

    def main(self):
        """
        Main Gui function which create Ui object,
        build interface and run the loop
        """
        self.ui = urwid.raw_display.Screen()
        self.ui.register_palette(self.palette)
        self.build_interface()
        self.ui.run_wrapper(self.run)

    def build_help(self):
        """ Fetch all key bindings and build help message """
        self.bindings = {}
        self.help_msg = []
        self.help_msg.append(
                urwid.AttrWrap(urwid.Text('\n Key bindings \n'), 'title'))
        self.help_msg.append(urwid.AttrWrap(urwid.Text(''), 'help'))
        for binding in self.config.parser.items('keybindings'):
            self.bindings[binding[0]] = binding[1]
            line = urwid.AttrWrap(
                    urwid.Text(
                            ' %s: %s ' % (binding[1], binding[0].replace('_', ' '))),
                    'help')
            self.help_msg.append(line)
        self.help_msg.append(urwid.AttrWrap(
                urwid.Text(' ctrl mouse-left: Open framework UI'), 'help'))
        self.help_msg.append(urwid.AttrWrap(urwid.Text(''), 'help'))
        self.help_msg.append(urwid.AttrWrap(
                urwid.Text(
                        ' Thanks for using Mesos-Viewer %s! ' % __version__, align='center'),
                'title'))
        self.help_msg.append(urwid.AttrWrap(urwid.Text(''), 'help'))
        self.help_msg.append(urwid.AttrWrap(urwid.Text(''), 'help'))
        self.help_msg.append(urwid.AttrWrap(urwid.Text(''), 'help'))
        self.help_msg.append(urwid.AttrWrap(urwid.Text(''), 'help'))

        self.help = Popup(self.help_msg, ('help', 'help'), (0, 1), self.view)


    def get_lable(self, label):
        switcher = {
            "name": (self.col_name, 1, 10),
            "cpus": (self.col_cpus, 6, 5),
            "memory": (self.col_memory, 5, 10),
            "uptime": (self.col_uptime, 4, 19)
        }
        return switcher.get(label, (self.col_name, 1, 10))

    def get_header_label(self, lable):
        heading, index, length = self.get_lable(lable)
        if lable in self.sort_on:
            return "{}{}".format(heading, self.sort_desc if self.sort_reverse else self.sort_asc)
        return heading

    def get_header_content(self):
        return [
            self.get_fixed_header(msg = ' N°', length = 4),
                         urwid.AttrWrap(urwid.Text(self.get_header_label("name"), align="center"), 'title'),
            ('fixed', 14, urwid.AttrMap(urwid.Text(self.total_frameworks, align="center"), 'name', 'focus')),
            ('fixed', 64, urwid.Columns(get_legend(), dividechars=0)),
            self.get_fixed_header(self.get_header_label("uptime"), length = 19),
            self.get_fixed_header(self.get_header_label("memory"), length = 10),
            self.get_fixed_header(self.get_header_label("cpus"), length = 5),
            self.get_fixed_header(msg = 'Tsks', length = 4),
            self.get_fixed_header(msg = 'Tsks', length = 20)
        ]

    def build_interface(self):
        """
        Build interface, refresh cache if needed, update frameworks listbox,
        create header, footer, view and the loop.
        """
        if self.cache_manager.is_outdated():
            self.cache_manager.refresh()

        self.frameworks = self.cache_manager.get_frameworks()

        self.update_frameworks(self.frameworks)
        if len(self.frameworks) > 0:
            self.total_frameworks = "Total: [{}]".format(str(len(self.frameworks)))
        # self.legend = get_legend()

        self.header_content = self.get_header_content()

        self.header = urwid.Columns(self.header_content, dividechars=1)

        self.footer_content = [
            urwid.AttrWrap(urwid.Text('', align="center"), 'title'),
            ('fixed', 35,
             urwid.Padding(urwid.AttrMap(urwid.Text('`h` HELP | `r` REFRESH | `q` QUIT', align='center'), 'footer')))
        ]

        self.footer = urwid.Columns(self.footer_content, dividechars=1)

        self.view = urwid.Frame(urwid.AttrWrap(self.listbox, 'body'), header=self.header, footer=self.footer)

        self.loop = urwid.MainLoop(
                self.view,
                self.palette,
                screen=self.ui,
                handle_mouse=True,
                unhandled_input=self.keystroke)

        self.build_help()
        self.already_build = True

    def get_fixed_header(self, msg = 'empty', style = 'header', align = 'center', length = 20):
        return ('fixed', length, urwid.Padding(urwid.AttrWrap(urwid.Text(msg, align=align), style)))



    def set_header_component(self, msg, section_id=1, style='title', align='center'):
        """ Set header message """
        self.header_content[section_id] = urwid.AttrWrap(
                urwid.Text(msg, align=align), style)
        self.view.set_header(urwid.Columns(self.header_content, dividechars=1))

    def sort_items(self):
        self.set_footer_component("Sorting by {} {}...".format(self.sort_on, "in reverse" if not self.sort_reverse else "") , 0)        
        threading.Thread(None, self.async_refresher, None, (), {'force': True}).start()
        self.view.set_header(urwid.Columns(self.get_header_content(), dividechars=1))


    def get_sorted(self, frameworks, by_key = 'name', reverse = False):
        return sorted(frameworks, key=attrgetter(by_key), reverse = self.sort_reverse)

    def update_frameworks(self, frameworks):
        """ Reload listbox and walker with new frameworks """
        items = []
        item_ids = []
        sn = 1
        for framework in self.get_sorted(frameworks, self.sort_on):
            items.append(ItemWidget(framework, sn))
            item_ids.append(framework.id)
            sn += 1

        if self.already_build:
            self.walker[:] = items
            self.update()
        else:
            self.walker = urwid.SimpleListWalker(items)
            self.listbox = urwid.ListBox(self.walker)



    def update(self):
        """ Update footer about focus framework """
        focus = self.listbox.get_focus()[0]
        msg = "submitted @ [%s], running since [%s]" % (focus.uptime, focus.uptime_descriptive)
        self.set_footer_component(msg=msg, section_id=0)



    def get_timer(self):
        return urwid.AttrWrap(urwid.Text(str(self.poller.counter), align="center"), 'title')


    def async_update_timer(self, counter=0, delay=10):
        remaining = int(delay - counter)
        self.set_header_component("Updating in {}s".format(str(remaining)), section_id=2, style='bad_name')
        self.loop.draw_screen()

    def async_refresher(self, which=None, header=None, force=False):
        if which is None:
            which = self.which
        if self.cache_manager.is_outdated(which) or force:
            self.cache_manager.refresh(which)
        frameworks = self.cache_manager.get_frameworks(which)
        self.update_frameworks(frameworks)
        if header is not None:
            self.set_header_component(header)
            self.which = which
        self.loop.draw_screen()


    def set_help(self):
        """ Set help msg in footer """
        self.set_footer_component(self.help, section_id=0, style='help')

    def set_footer(self, msg, style="normal"):
        """ Set centered footer message """
        if style == "normal":
            self.footer = urwid.AttrWrap(urwid.Text(msg), 'footer')
            self.view.set_footer(self.footer)
        elif style == "error":
            self.footer = urwid.AttrWrap(urwid.Text(msg), 'footer-error')
            self.view.set_footer(self.footer)

    def set_footer_component(self, msg, section_id=1, style='footer', align='left'):
        """ Set footer  message """
        self.footer_content[section_id] = urwid.AttrWrap(urwid.Text(msg, align=align), style)
        self.view.set_footer(urwid.Columns(self.footer_content, dividechars=1))


    def keystroke(self, user_input):
        """ All key bindings are computed here """
        # QUIT
        if user_input in ('q', 'Q'):
            self.exit(must_raise=True)

        if user_input in self.bindings['open_framework_link'].split(','):
            self.open_webbrowser(self.listbox.get_focus()[0].url)
        if user_input in self.bindings['show_framework_link'].split(','):
            self.set_footer_component(msg=self.listbox.get_focus()[0].url, section_id=0)

        # MOVEMENTS
        if user_input in self.bindings['down'].split(',') and self.listbox.focus_position - 1 in self.walker.positions():
            self.listbox.set_focus(
                    self.walker.prev_position(self.listbox.focus_position))
        if user_input in self.bindings['up'].split(',') and self.listbox.focus_position + 1 in self.walker.positions():
            self.listbox.set_focus(
                    self.walker.next_position(self.listbox.focus_position))
        if user_input in self.bindings['page_up'].split(','):
            self.listbox._keypress_page_up(self.ui.get_cols_rows())
        if user_input in self.bindings['page_down'].split(','):
            self.listbox._keypress_page_down(self.ui.get_cols_rows())
        if user_input in self.bindings['first_framework'].split(','):
            self.listbox.set_focus(self.walker.positions()[0])
        if user_input in self.bindings['last_framework'].split(','):
            self.listbox.set_focus(self.walker.positions()[-1])

        # SORT
        if user_input in self.bindings['sort_by_name'].split(','):
            self.sort_on = "name"
            self.sort_reverse = not self.sort_reverse
            self.sort_items()
        if user_input in self.bindings['sort_by_cpu'].split(','):
            self.sort_on = "cpus"
            self.sort_reverse = not self.sort_reverse
            self.sort_items()
        if user_input in self.bindings['sort_by_mem'].split(','):
            self.sort_on = "memory"
            self.sort_reverse = not self.sort_reverse
            self.sort_items()
        if user_input in self.bindings['sort_by_uptime'].split(','):
            self.sort_on = "uptime"
            self.sort_reverse = not self.sort_reverse
            self.sort_items()

        # OTHERS
        if user_input in self.bindings['refresh'].split(','):
            self.set_footer_component('Refreshing new frameworks...', 0)
            threading.Thread(None, self.async_refresher, None, (), {'force': True}).start()

        if user_input in self.bindings['reload_config'].split(','):
            self.reload_config()
        if user_input in ('h', 'H', '?'):
            keys = True
            while True:
                if keys:
                    self.ui.draw_screen(
                            self.ui.get_cols_rows(),
                            self.help.render(self.ui.get_cols_rows(), True))
                    keys = self.ui.get_input()
                    if 'h' or 'H' or '?' or 'escape' in keys:
                        break
        # MOUSE
        if len(user_input) > 1 and user_input[0] == 'ctrl mouse release':
            self.open_webbrowser(self.listbox.get_focus()[0].url)

    def reload_config(self):
        """
        Create new Config object, reload colors, refresh cache
        if needed and redraw screen.
        """
        self.set_footer_component(msg='Reloading configuration', section_id=0)
        self.config = Config()
        self.build_help()
        self.palette = self.config.get_palette()
        self.build_interface()
        self.loop.draw_screen()
        self.set_footer_component(msg='Configuration file reloaded!', section_id=0)

        if self.config.parser.get('settings', 'cache') != self.cache_manager.cache_path:
            self.cache_manager.cache_path = self.config.parser.get('settings', 'cache')

    def open_webbrowser(self, url):
        """ Handle url and open sub process with web browser """
        if self.config.parser.get('settings', 'browser_cmd') == "__default__":
            python_bin = sys.executable
            subprocess.Popen(
                    [python_bin, '-m', 'webbrowser', '-t', url],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)
        else:
            cmd = self.config.parser.get('settings', 'browser_cmd')
            try:
                p = subprocess.Popen(
                        cmd.replace('__url__', url),
                        shell=True,
                        close_fds=True,
                        stderr=subprocess.PIPE)

                return_code = p.wait()
            except KeyboardInterrupt:
                stderr = "User keyboard interrupt detected!"
                self.set_footer_component(msg=stderr, section_id=0, style="footer-error")
                return
            if return_code > 0:
                stderr = p.communicate()[1]
                self.set_footer_component(msg="%s" % stderr, section_id=0, style="footer-error")

    def exit(self, must_raise=False):
        self.poller.is_running = False
        self.poller.join()
        if must_raise:
            raise urwid.ExitMainLoop()
        urwid.ExitMainLoop()

    def run(self):
        urwid.connect_signal(self.walker, 'modified', self.update)

        try:
            self.poller.start()
            self.loop.run()
        except KeyboardInterrupt:
            self.exit()
        print('Exiting...!!')


def get_legend():
    lst = [
        urwid.AttrMap(urwid.Text("STG:", align="left"), 'body', 'focus'), get_staging_status(),
        urwid.AttrMap(urwid.Text("STR:", align="left"), 'body', 'focus'), get_starting_status(),
        urwid.AttrMap(urwid.Text("RUN:", align="left"), 'body', 'focus'), get_running_status(),
        urwid.AttrMap(urwid.Text("URC:", align="left"), 'body', 'focus'), get_unreachable_status(),
        urwid.AttrMap(urwid.Text("FIN:", align="left"), 'body', 'focus'), get_finished_status(),
        urwid.AttrMap(urwid.Text("KIL:", align="left"), 'body', 'focus'), get_killing_status(),
        urwid.AttrMap(urwid.Text("KLD:", align="left"), 'body', 'focus'), get_killed_status(),
        urwid.AttrMap(urwid.Text("FLD:", align="left"), 'body', 'focus'), get_failed_status(),
        urwid.AttrMap(urwid.Text("LST:", align="left"), 'body', 'focus'), get_lost_status()
    ]
    return lst


def get_staging_status():
    return urwid.AttrMap(urwid.Text("○", align="center"), 'name', 'focus')


def get_starting_status():
    return urwid.AttrMap(urwid.Text("◒", align="center"), 'name', 'focus')


def get_running_status():
    return urwid.AttrMap(urwid.Text("●", align="center"), 'name', 'focus')


def get_unreachable_status():
    return urwid.AttrMap(urwid.Text("○", align="center"), 'bad_name', 'focus')


def get_finished_status():
    return urwid.AttrMap(urwid.Text("◕", align="center"), 'bad_name', 'focus')


def get_killing_status():
    return urwid.AttrMap(urwid.Text("◐", align="center"), 'bad_name', 'focus')


def get_killed_status():
    return urwid.AttrMap(urwid.Text("◑", align="center"), 'bad_name', 'focus')


def get_failed_status():
    return urwid.AttrMap(urwid.Text("●", align="center"), 'bad_name', 'focus')


def get_lost_status():
    return urwid.AttrMap(urwid.Text("◓", align="center"), 'bad_name', 'focus')