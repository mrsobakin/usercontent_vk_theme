from colorsys import rgb_to_hsv, hsv_to_rgb


def hex_to_rgb(hex):
    return [ int(hex[i:i+2], base=16)/255 for i in range(0, len(hex), 2) ]

def rgb_to_hex(color):
    return '%02x%02x%02x' % tuple( int(255*c) for c in color )


def mix_rgb(a, b, x):
    return [ ai*x+bi*(1-x) for ai, bi in zip(a,b) ]


def make_filter(a, b):
    mult, add = [], []
    for ai, bi in zip(a, b):
        if ai != 0:
            mult.append(bi/ai)
            add.append(0)
        else:
            mult.append(256)
            add.append(bi)
    
    return f"""url(\'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg"><filter id="colorize"><feColorMatrix color-interpolation-filters="sRGB" type="matrix" values=" {mult[0]} 0 0 0 {add[0]} 0 {mult[1]} 0 0 {add[1]} 0 0 {mult[2]} 0 {add[2]} 0 0 0 1 0"/></filter></svg>#colorize\')"""


PAGE_CHAIN = hex_to_rgb("5181b8")
PROGRESS_BAR = hex_to_rgb("6b8fb5")


def generate_vk_theme(accent_hex, accent_darker_hex=None):
    accent = hex_to_rgb(accent_hex)

    if not accent_darker_hex:
        accent_hsv = rgb_to_hsv(*accent)
        
        # Magic values are vk's blue and azure colors difference
        accent_darker_hex = rgb_to_hex(
            hsv_to_rgb(
                accent_hsv[0],
                min(1, accent_hsv[1]*1.389),
                accent_hsv[2]*0.868
            )
        )

    chain_filter_str = make_filter(PAGE_CHAIN, accent)
    pbar_filter_str = make_filter(PROGRESS_BAR, accent)

    return f"""@-moz-document domain(vk.com) {{
    [scheme=vkcom_dark] {{
        --accent: #{accent_hex} !important;
        --accent-darker: #{accent_darker_hex} !important;
        
        --im_text_name: var(--accent) !important;
        --text_link: var(--accent) !important;
        --blue_400: var(--accent) !important;
        
        --header_tab_active_indicator: var(--accent-darker) !important;
        --tabbar_tablet_active_icon: var(--accent-darker) !important;
        --text_link_highlighted_background: var(--accent-darker) !important;
        --dynamic_blue: var(--accent-darker) !important;
        
        --gray_20: #7c7c7c !important;
        --gray_40: #7a7a7a !important;
        --gray_70: #2a2a2a !important;
        --gray_100_alpha60: rgba(168, 170, 172, 0.60) !important;
        --gray_700: #2a2a2a !important;
        --gray_700_alpha60: rgba(63, 63, 63, 0.60) !important;
        --gray_750: #242424 !important;
        --gray_800: #191919 !important;
        --gray_800_alpha72: rgba(38, 38, 38, 0.72) !important;
        --gray_800_alpha88: rgba(38, 38, 38, 0.88) !important;
        --gray_850: #141414 !important;
        --gray_900: #111111 !important;
        --gray_900_alpha16: rgba(25, 25, 25, 0.16) !important;
        --gray_900_alpha72: rgba(25, 25, 25, 0.72) !important;
        --gray_900_alpha88: rgba(25, 25, 25, 0.88) !important;
        --gray_940: #0a0a0a !important;
        --gray_960: #050505 !important;
    }}

    /*   online icons   */
    [dir] .online.mobile::after {{
        background-image: url(data:image/svg+xml;charset=utf-8,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%227%22%20height%3D%2211%22%3E%3Cpath%20fill%3D%22%23{accent_hex}%22%20fill-rule%3D%22evenodd%22%20d%3D%22M0%201.5C0%20.7.7%200%201.5%200h4C6.3%200%207%20.7%207%201.5v8c0%20.8-.7%201.5-1.5%201.5h-4A1.5%201.5%200%20010%209.5v-8zM1%202h5v6H1V2z%22%2F%3E%3C%2Fsvg%3E) !important;
        background-color: var(--online-badge-background) !important;
    }}
    
    [dir] .nim-dialog:not(.nim-dialog_deleted):not(.nim-dialog_classic).nim-dialog_selected .nim-dialog--photo .online.mobile::after {{
        background-image: url(data:image/svg+xml;charset=utf-8,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%227%22%20height%3D%2211%22%3E%3Cpath%20fill%3D%22%23ffffff%22%20fill-rule%3D%22evenodd%22%20d%3D%22M0%201.5C0%20.7.7%200%201.5%200h4C6.3%200%207%20.7%207%201.5v8c0%20.8-.7%201.5-1.5%201.5h-4A1.5%201.5%200%20010%209.5v-8zM1%202h5v6H1V2z%22%2F%3E%3C%2Fsvg%3E) !important;
        background-color: var(--online-badge-background) !important;
    }}
    
    [dir] .online::after {{
        background-color: var(--accent) !important;
    }}

    [dir] .nim-dialog:not(.nim-dialog_deleted):not(.nim-dialog_classic).nim-dialog_selected .nim-dialog--photo .online::after {{
        background-color: #fff !important;
    }}

    /*   page chain icon   */
    .ownerButton__icon {{
        filter: {chain_filter_str};
    }}
    
    /*   checkboxes   */
    [dir] [scheme="vkcom_dark"] .settings_narrow_row input[type="checkbox"]:checked + label::before {{
        background-image: url(data:image/svg+xml;charset=utf-8,%3Csvg%20width%3D%2220%22%20height%3D%2220%22%20fill%3D%22none%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Cpath%20fill-rule%3D%22evenodd%22%20clip-rule%3D%22evenodd%22%20d%3D%22M2.44%204.18C2%205.04%202%206.16%202%208.4v3.2c0%202.24%200%203.36.44%204.22a4%204%200%20001.74%201.74c.86.44%201.98.44%204.22.44h3.2c2.24%200%203.36%200%204.22-.44a4%204%200%20001.74-1.74c.44-.86.44-1.98.44-4.22V8.4c0-2.24%200-3.36-.44-4.22a4%204%200%2000-1.74-1.74C14.96%202%2013.84%202%2011.6%202H8.4c-2.24%200-3.36%200-4.22.44a4%204%200%2000-1.74%201.74zm12.2%203.8a.9.9%200%2010-1.28-1.27L8.7%2011.38%206.64%209.33a.9.9%200%2000-1.28%201.27l2.7%202.69a.9.9%200%20001.27%200l5.3-5.3z%22%20fill%3D%22%23{accent_hex}%22%2F%3E%3C%2Fsvg%3E) !important;
    }}
    
    /*   vk logo   */
    .TopHomeLink > svg:nth-child(1) > g:nth-child(1) > g:nth-child(1) > path:nth-child(2) {{
        fill: var(--accent-darker) !important;
    }}
    
    /*   progress bar   */
    [dir] .ui_progress .ui_progress_back {{
        background-color: var(--background_light) !important;
        border: 1px solid var(--separator_common) !important;
    }}
    
    [dir] .ui_progress .ui_progress_bar {{
        filter: {pbar_filter_str};
    }}
}}"""


if __name__ == "__main__":
    from sys import argv
    print(generate_vk_theme(argv[1]))
