// mindpalace desktop shell — spawns the daemon sidecar, waits for its port,
// then opens the window on the local GUI. The webview is just another client
// of the same localhost API every other surface uses.
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::net::TcpStream;
use std::sync::Mutex;
use std::time::Duration;

use tauri::Manager;
use tauri_plugin_shell::process::CommandChild;
use tauri_plugin_shell::ShellExt;

const PORT: u16 = 7777;

struct Sidecar(Mutex<Option<CommandChild>>);

fn port_open(port: u16) -> bool {
    TcpStream::connect_timeout(&([127, 0, 0, 1], port).into(), Duration::from_millis(300)).is_ok()
}

fn wait_port(port: u16, secs: u64) -> bool {
    for _ in 0..secs * 10 {
        if port_open(port) {
            return true;
        }
        std::thread::sleep(Duration::from_millis(100));
    }
    false
}

fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .setup(|app| {
            // a daemon already listening (dev `mindpalace serve`) is reused;
            // otherwise spawn our bundled sidecar
            let child = if port_open(PORT) {
                None
            } else {
                let (_rx, child) = app
                    .shell()
                    .sidecar("mindpalaced")?
                    .args(["--port", &PORT.to_string()])
                    .spawn()?;
                Some(child)
            };
            app.manage(Sidecar(Mutex::new(child)));
            wait_port(PORT, 30); // window opens regardless; the UI reloads fine

            let url = format!("http://127.0.0.1:{PORT}").parse().unwrap();
            tauri::WebviewWindowBuilder::new(app, "main", tauri::WebviewUrl::External(url))
                .title("mindpalace")
                .inner_size(1360.0, 860.0)
                .min_inner_size(800.0, 560.0)
                .build()?;
            Ok(())
        })
        .build(tauri::generate_context!())
        .expect("failed to build mindpalace desktop")
        .run(|app, event| {
            if let tauri::RunEvent::Exit = event {
                if let Some(s) = app.try_state::<Sidecar>() {
                    if let Some(child) = s.0.lock().unwrap().take() {
                        let _ = child.kill(); // the daemon dies with the app
                    }
                }
            }
        });
}
