TODO
===============================================================================
- UI Plugins
    - Create a default one for GTK+
    - Add loaded plugins and selected plugins methods which returns a list of names
    - Need to convert wpmaker.py main() method into a class which can be passed
to ui plugins

- Plugins
    - Add ui hooks as they are implemented in Application class

- Multi monitor support
- Multiple `wallpaper_queue` Wallpapers class

- `RecursiveSplit` plugin
    - Split chance option

Bugs
===============================================================================
- If verbose is set in config file the log doesnt show plugin loading because
the config has to be checked after plugins are loaded
