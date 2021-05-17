import cx_Freeze

executables = [cx_Freeze.Executable("main.py", base = "Win32GUI" )]

cx_Freeze.setup(
    name="Gua Game",
    options={"build_exe": {"packages":["pygame", 'socket', 'sys'],
                           "include_files":['background.png', 'gua_head.png', 'gua_smile.png', 'gua_blush.png', 'wall_body.png', 'wall_head.png']}},
    executables = executables)