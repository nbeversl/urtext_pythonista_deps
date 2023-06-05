from urtext_pythonista import UrtextEditor
from urtext_theme_light import urtext_theme_light
from urtext_theme_light_custom import urtext_theme_light_custom

s = UrtextEditor({    
    'path' : '/private/var/mobile/Library/Mobile Documents/iCloud~com~omz-software~Pythonista3/Documents/Urtext Projects/small test project',        
    'theme' : urtext_theme_light_custom,    
    # 'launch_action' : 'new_node',
})
s.show()
