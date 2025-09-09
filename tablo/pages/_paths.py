from pathlib import Path

def get_data_dir(folder_name: str) -> Path:
    """Znajdź katalog z danymi, testując kilka sensownych lokalizacji."""
    here = Path(__file__).parent            
    candidates = [
        here / folder_name,                 
        here.parent / folder_name,          
        here.parent / 'assets' / folder_name,
        Path.cwd() / folder_name,           
        here.parent.parent / folder_name,   
    ]
    for p in candidates:
        if p.exists():
            return p
        
    return candidates[1]