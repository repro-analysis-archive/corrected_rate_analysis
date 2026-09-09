function S = jiim_style_r7()
% House style for the JIIM R7 final figure round. Palette and typography per
% FIGURE_TEMPLATE_unified_v9.md sections 2-1 and 2-2. Grayscale + one navy accent.
S.navy   = [0.170 0.239 0.420];   % #2B3D6B  primary accent (the only accent)
S.dark   = [0.302 0.302 0.302];   % #4D4D4D  strong secondary
S.medium = [0.420 0.420 0.420];   % #6B6B6B  ordinary secondary
S.second = [0.541 0.541 0.541];   % #8A8A8A  residual / zero reference
S.guide  = [0.702 0.702 0.702];   % #B3B3B3  guide / separator / connector
S.vlight = [0.816 0.816 0.816];   % #D0D0D0  sparingly
S.text   = [0.102 0.102 0.102];   % #1A1A1A  text / axes / marker edge
S.ftick  = 14;  S.faxis = 15;  S.fpanel = 16;      % tick -> axis -> panel
S.width_cm = 17.4;                                  % 174.0 mm final design width
S.mk_fill  = 3.20;   % ~1.13 mm diameter  (1 pt = 0.3528 mm)
S.mk_open  = 3.60;   % ~1.27 mm  hollow / angular markers read smaller
S.ci_lw    = 1.30;   % pt - kept below the marker diameter so the point stays legible
S.mk_edge  = 0.80;   % pt
% Final polish round: the v9 hexes are unchanged, but every element that had been sitting on the
% lightest role is promoted one step darker so it survives print and reduction.
S.zero     = S.medium;   % zero reference line   #8A8A8A -> #6B6B6B
S.conn     = S.second;   % H1-H2 / paired connectors  #B3B3B3 -> #8A8A8A
S.softedge = S.second;   % secondary box outlines     #B3B3B3 -> #8A8A8A
S.gridA    = 0.55;       % x guide alpha on #B3B3B3   0.35 -> 0.55
end
