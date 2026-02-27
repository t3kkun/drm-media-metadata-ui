import flet as ft
import csv
import os
import webbrowser
from collections import defaultdict

def main(page: ft.Page):
    page.title = "DMM Private Library Viewer"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20

    # CSVデータの読み込み
    library_data = []
    csv_path = "dmm_library.csv"

    if os.path.exists(csv_path):
        with open(csv_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                library_data.append(row)
    
    # CSVのフルパスに基づいてディレクトリごとに分類
    def organize_by_directory():
        dir_structure = defaultdict(list)
        
        for item in library_data:
            full_path = item.get("フルパス", "")
            if full_path:
                # ファイルの親ディレクトリを取得
                dir_path = os.path.dirname(full_path)
                # 相対パスに変換（contents基準）
                contents_dir = os.path.join(os.getcwd(), "contents")
                try:
                    rel_dir = os.path.relpath(dir_path, contents_dir)
                    if rel_dir == ".":
                        rel_dir = "Root"
                except ValueError:
                    rel_dir = "Other"
                
                dir_structure[rel_dir].append(item)
        
        return dir_structure
    
    # ディレクトリ構造を取得
    dir_structure = organize_by_directory()

    def play_video(path: str):
        try:
            os.startfile(path)
            page.snack_bar = ft.SnackBar(ft.Text(f"Starting: {os.path.basename(path)}"))
            page.snack_bar.open = True
            page.update()
        except Exception as ex:
            print(f"Error opening file: {ex}")

    def open_dmm_page(cid: str):
        # 指定のURL形式
        url = f"https://video.dmm.co.jp/av/content/?id={cid}"
        try:
            webbrowser.open(url)
            page.snack_bar = ft.SnackBar(ft.Text("Opened DMM page in browser."))
            page.snack_bar.open = True
            page.update()
        except Exception as ex:
            print(f"Error opening URL: {ex}")

    def create_grid_for_files(csv_items: list, search_term: str = ""):
        """指定されたCSVレコードリストに基づいてグリッドを作成"""
        grid = ft.GridView(
            runs_count=5,
            max_extent=400,
            child_aspect_ratio=0.6,
            spacing=15,
            run_spacing=15,
        )
        
        st = (search_term or "").lower()
        
        for csv_item in csv_items:
            title = csv_item.get("タイトル", "")
            cid = csv_item.get("ID", "")
            thumb = csv_item.get("サムネURL", "")
            full_path = csv_item.get("フルパス", "")
            filename = csv_item.get("ファイル名", "")
            
            # 検索フィルタ
            if st in title.lower() or st in cid.lower() or st in filename.lower():
                # 画像部分だけタップで再生
                thumb_area = ft.GestureDetector(
                    on_tap=lambda e, p=full_path: play_video(p),
                    mouse_cursor=ft.MouseCursor.CLICK,
                    content=ft.Image(
                        src=thumb,
                        fit="cover",
                        repeat=ft.ImageRepeat.NO_REPEAT,
                        gapless_playback=True,
                    ) if thumb else ft.Container(
                        bgcolor="#1e1e1e",
                        content=ft.Text("No thumbnail", text_align="center"),
                    ),
                )

                # 下部：タイトル + ボタン
                footer = ft.Container(
                    padding=8,
                    content=ft.Column(
                        [
                            ft.Text(
                                title if title else filename,
                                size=11,
                                weight="bold",
                                max_lines=2,
                                overflow="ellipsis",
                            ),
                            ft.Row(
                                [
                                    ft.IconButton(
                                        icon=ft.Icons.OPEN_IN_NEW,
                                        tooltip="DMM作品ページを開く",
                                        on_click=lambda e, c=cid: open_dmm_page(c) if cid else None,
                                    ) if cid else ft.Container(width=40),
                                    ft.Text(
                                        cid if cid else filename,
                                        size=10,
                                        opacity=0.7,
                                        overflow="ellipsis",
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                        ],
                        spacing=4,
                        tight=True,
                    ),
                )

                card = ft.Card(
                    elevation=2,
                    content=ft.Container(
                        content=ft.Column([thumb_area, footer], spacing=0, tight=True),
                    ),
                )

                grid.controls.append(card)
        
        return grid

    # 検索フィールドと更新関数
    search_field = ft.TextField(
        label="Search by title or ID",
        prefix_icon=ft.Icons.SEARCH,
    )
    
    def update_display(search_term: str = ""):
        """全ディレクトリの内容を更新"""
        dir_keys = sorted(dir_structure.keys())
        content_items = []
        
        for directory in dir_keys:
            csv_items = dir_structure[directory]
            grid = create_grid_for_files(csv_items, search_term)
            
            # ディレクトリ名と件数をヘッダーとして表示
            header = ft.Container(
                content=ft.Text(
                    f"{directory} ({len(grid.controls)})",
                    size=18,
                    weight="bold",
                    color="#4CAF50",
                ),
                padding=ft.padding.only(top=20, left=10, right=10, bottom=10),
            )
            
            content_items.append(header)
            content_items.append(grid)
        
        # 全コンテンツをスクロールビューで表示
        page.clean()
        page.add(
            ft.Row(
                [ft.Text("Available contents [LOCAL]", size=30, weight="bold")],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            search_field,
            ft.ListView(
                controls=content_items,
                expand=True,
                spacing=0,
            ),
        )
    
    def on_search_change(e):
        update_display(search_field.value)

    search_field.on_change = on_search_change

    update_display()

if __name__ == "__main__":
    ft.run(main)
