import json

def analyze_funing_gaps():
    with open('full_lexicon_translated.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    missing_mun = [i for i in data if not i.get('raw_text')]
    missing_vi = [i for i in data if not i.get('vietnamese')]
    
    print(f"Total entries: {len(data)}")
    print(f"Entries missing Mun (Dao): {len(missing_mun)}")
    print(f"Entries missing Vietnamese: {len(missing_vi)}")
    
    print("\nSample missing Mun:")
    for i in missing_mun[:5]:
        print(f"ID: {i['entry_id']} | EN: {i['meaning_en']}")

if __name__ == "__main__":
    analyze_funing_gaps()
