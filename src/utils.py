def get_typing_indicator_html(label_text="Thinking"):
    return f"""
    <div class="thinking-wrap">
      <span class="label">{label_text}</span>
      <span class="dot dot1"></span>
      <span class="dot dot2"></span>
      <span class="dot dot3"></span>
    </div>

    <style>
    .thinking-wrap {{
      font-family: 'Arial', sans-serif;
      color: #666;
      font-size: 16px;
      display: flex;
      align-items: center;
      gap: 4px;
      padding: 6px 0;
    }}
    .label {{
      font-weight: bold;
    }}
    .dot {{
      width: 6px;
      height: 6px;
      background: #666;
      border-radius: 50%;
      animation: blink 1s infinite ease-in-out;
    }}
    .dot2 {{ animation-delay: 0.2s; }}
    .dot3 {{ animation-delay: 0.4s; }}

    @keyframes blink {{
      0%, 100% {{ opacity: 0.2; transform: translateY(0); }}
      50% {{ opacity: 1; transform: translateY(-4px); }}
    }}
    </style>
    """