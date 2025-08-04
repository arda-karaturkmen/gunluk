# Bu dosyanın içeriğini PythonAnywhere'deki 'Web' sekmesinde bulunan
# 'WSGI configuration file' bölümüne yapıştırmanız gerekmektedir.
# '/home/ardakaraturkmen/gunluk' kısmını kendi sunucu yolunuzla güncellemeyi unutmayın.

import os
import sys

# Proje dizininizi Python yoluna ekleyin
# ardakaraturkmen yazan yeri kendi PythonAnywhere kullanıcı adınızla değiştirin.
# 'gunluk' kısmını da projenizi yüklediğiniz klasörün adıyla değiştirin.
path = '/home/ardakaraturkmen/gunluk'
if path not in sys.path:
    sys.path.insert(0, path)

# Sanal ortamınızı (virtualenv) aktif etmek için (eğer kullanıyorsanız)
# activate_this = '/home/ardakaraturkmen/.virtualenvs/my-virtualenv/bin/activate_this.py'
# with open(activate_this) as f:
#     exec(f.read(), dict(__file__=activate_this))

# Django ayar dosyasını belirtin
os.environ['DJANGO_SETTINGS_MODULE'] = 'social_diary.settings'

# WSGI uygulamasını yükleyin
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
