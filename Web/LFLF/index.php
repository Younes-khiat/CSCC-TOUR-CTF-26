<!DOCTYPE html>
<html>
<head>
    <title>Document Viewer - CTF Challenge</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Courier New', monospace; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { 
            max-width: 900px; 
            margin: 0 auto; 
            background: white; 
            padding: 30px; 
            border-radius: 10px; 
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        }
        h1 { 
            color: #667eea; 
            margin-bottom: 10px;
            text-align: center;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 14px;
        }
        .nav { 
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            padding: 15px;
            background: #f5f5f5;
            border-radius: 5px;
            flex-wrap: wrap;
        }
        .nav a { 
            padding: 8px 15px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 4px;
            transition: all 0.3s;
        }
        .nav a:hover { 
            background: #764ba2;
            transform: translateY(-2px);
        }
        .content { 
            background: #f9f9f9;
            padding: 20px;
            border-radius: 5px;
            border-left: 4px solid #667eea;
            min-height: 200px;
            white-space: pre-wrap;
            font-family: 'Courier New', monospace;
        }
        .welcome {
            color: #333;
            line-height: 1.8;
        }
        .footer {
            margin-top: 30px;
            text-align: center;
            color: #999;
            font-size: 12px;
        }
        .hint {
            background: #fff3cd;
            border: 1px solid #ffc107;
            padding: 10px;
            border-radius: 4px;
            margin-bottom: 20px;
            font-size: 13px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📄 Secure Document Viewer</h1>
        <p class="subtitle">Company Internal Documentation System v1.0</p>
        
        <div class="hint">
            💡 <strong>Hint:</strong> Our flag is hidden somewhere in the system files. Can you find it?
        </div>
        
        <div class="nav">
            <a href="?page=home">🏠 Home</a>
            <a href="?page=about">ℹ️ About</a>
            <a href="?page=contact">📧 Contact</a>
            <a href="?page=docs">📚 Documentation</a>
        </div>
        
        <div class="content">
<?php
$flag_file = '../flag.txt';
if (!file_exists($flag_file)) {
    file_put_contents($flag_file, 'CSCC{l0c4l_f1l3_3xplos10n}');
}

// Vulnerable parameter - no sanitization!
$page = isset($_GET['page']) ? $_GET['page'] : 'home';

// Define pages
$pages = [
    'home' => "
<div class='welcome'>
<h2> Document Viewer </h2>
<br>
<br>

</div>
    ",
    'about' => "

<h2>Documentation</h2>
<br>
<strong>Available Documents:</strong>
<br><br>
1. User Manual (Coming Soon)
<br>
2. API Documentation (Coming Soon)
<br>
3. Security Guidelines (Coming Soon)
<br><br>
Check back later for updates!
</div>
    "
];

if (array_key_exists($page, $pages)) {
    echo $pages[$page];
} else {
    $file = $page . '.php';
    
    if (file_exists($file)) {
        include($file);
    } else {
        if (file_exists($page)) {
            echo "<strong>File Contents:</strong><br><br>";
            echo htmlspecialchars(file_get_contents($page));
        } else {
            echo "<div class='welcome'>";
            echo "<h2>❌ Page Not Found</h2>";
            echo "<br>The requested page could not be found.";
            echo "<br><br>Maybe you should try looking elsewhere... 🤔";
            echo "</div>";
        }
    }
}
?>
        </div>
        
        <div class="footer">
            <p>CSCC tour CTF</p>
        </div>
    </div>
</body>
</html>
