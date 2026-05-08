import tokens from './tokens.json';

const { primitive: p, semantic: s } = tokens;

export const Theme = {
  colors: {
    // 백엔드와 공유하는 핵심 컬러 (tokens.json 구조 유지)
    primary: p[s.header_bg] || p.nissan_blue, 
    onPrimary: p[s.header_font] || p.white,
    
    // 프론트엔드 전용 컬러 (tokens.json에 추가한 값들)
    background: p[s.app_background],
    disabled: p.app_disabled,
    terminal: p[s.app_terminal],
    terminalText: p[s.app_terminal_text],
    textMain: p[s.body_font] || p.black
  },
  layout: {
    padding: 40,
    radius: 10,
    buttonWidth: '48%'
  }
};
