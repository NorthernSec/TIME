# Plugins

Put your plug-ins in this folder, and edit the `./etc/plugins.txt` file.
 Under **plugin**, write the name of the library without the `.py`
 extention. <br />
Under **state**, put `load` or `enable` to enable it. Any
 other word will disable the plug-in. <br />
Under **args**, you can pass arguments to the plug-in, if it takes any.
 the format is `key=value`, without a space. Only pass arguments if the
 plug-in takes any, otherwise loading the plug-in will fail.
