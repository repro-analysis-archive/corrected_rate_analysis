% make_Fig1.m — corrected analytic framework (R7). Native MATLAB vector shapes only.
% (A) cohort and split; (B) the four questions. Class V. No bitmap, no tracing.
S = jiim_style_r7();
% Fig1-only micro-adjustment (2026-09-09): the two secondary grey roles are ~15% darker in CIELAB L* so the
% HER2-positive and empty-arm branches read more clearly; the navy primary pathway, the near-black text and
% the flow connectors are unchanged. jiim_style_r7.m is shared by Fig2-5 and is deliberately untouched.
S.softedge = [116 116 116]/255;   % #747474  secondary box outlines + empty-arm stub  (was #8A8A8A, L* 57.5 -> 48.8)
S.gtext    = [ 90  90  90]/255;   % #5A5A5A  secondary-branch and caption text       (was #6B6B6B, L* 45.2 -> 38.2)
here = fileparts(mfilename('fullpath'));
D = load(fullfile(here,'..','..','figure_data','fig_data_r7.mat'));
outdir = fullfile(here,'..','..','reproduction','figures');
n980=D.n980; n739=D.n739; n241=D.n241; nH1=D.nH1; nH2=D.nH2; n728=D.n728;
assert(n980==980 && n739==739 && n241==241 && nH1==370 && nH2==369 && n728==728, ...
       'Fig1: canonical cohort counts failed');

fig = figure('Color',[1 1 1],'Units','centimeters','Position',[2 2 S.width_cm 11.2]);
fs = S.ftick-2; fsn = S.ftick-2;

% ================= Panel A =================
axA = axes('Parent',fig,'Units','normalized','Position',[0.035 0.335 0.945 0.605]);
hold(axA,'on'); axis(axA,[0 1 0 1]); axis(axA,'off');


white=[1 1 1]; pale=[0.973 0.973 0.973];
% root
box_(axA,0.50,0.905,0.40,0.155,S.navy,1.2,pale);
txt_(axA,0.50,0.945,'MAMA-MIA / I-SPY2 cohort',fs,S.text,'normal');
txt_(axA,0.50,0.872,sprintf('n = %d',n980),fsn,S.navy,'bold');
% bus to the two cohorts
seg_(axA,0.50,0.827,0.50,0.775,S.medium,1.1);
seg_(axA,0.29,0.775,0.80,0.775,S.medium,1.1);
seg_(axA,0.29,0.775,0.29,0.735,S.medium,1.1);
seg_(axA,0.80,0.775,0.80,0.735,S.medium,1.1);
% HER2-negative (primary)
box_(axA,0.29,0.640,0.36,0.190,S.navy,1.2,pale);
txt_(axA,0.29,0.700,'HER2-negative',fs,S.text,'normal');
txt_(axA,0.29,0.640,sprintf('n = %d',n739),fsn,S.navy,'bold');
txt_(axA,0.29,0.583,'primary',fs-1,S.gtext,'normal');
% HER2-positive (secondary weight)
box_(axA,0.80,0.640,0.36,0.190,S.softedge,1.0,white);
txt_(axA,0.80,0.700,'HER2-positive',fs,S.gtext,'normal');
txt_(axA,0.80,0.640,sprintf('n = %d',n241),fsn,S.gtext,'normal');
txt_(axA,0.80,0.583,'exploratory / descriptive only',fs-1,S.gtext,'normal');
% two PARALLEL children of HER2-negative: the split, and the empty-arm sensitivity
seg_(axA,0.29,0.545,0.29,0.500,S.medium,1.1);
seg_(axA,0.175,0.500,0.545,0.500,S.medium,1.1);
seg_(axA,0.175,0.500,0.175,0.455,S.medium,1.1);
seg_(axA,0.545,0.500,0.545,0.455,S.softedge,1.0);
box_(axA,0.175,0.380,0.30,0.150,S.navy,1.2,pale);
txt_(axA,0.175,0.418,'fixed random 50/50 split',fs-1,S.text,'normal');
txt_(axA,0.175,0.352,'seed 42',fs-1,S.gtext,'normal');
box_(axA,0.545,0.380,0.36,0.150,S.softedge,1.0,white);
txt_(axA,0.545,0.418,'empty-arm exclusion sensitivity',fs-1,S.gtext,'normal');
txt_(axA,0.545,0.352,sprintf('n = %d',n728),fsn-1,S.gtext,'normal');
% H1 / H2
seg_(axA,0.175,0.305,0.175,0.255,S.medium,1.1);
seg_(axA,0.070,0.255,0.280,0.255,S.medium,1.1);
seg_(axA,0.070,0.255,0.070,0.210,S.medium,1.1);
seg_(axA,0.280,0.255,0.280,0.210,S.medium,1.1);
box_(axA,0.070,0.140,0.135,0.140,S.navy,1.2,pale);
txt_(axA,0.070,0.175,'H1',fs,S.text,'bold');
txt_(axA,0.070,0.112,sprintf('n = %d',nH1),fsn-1,S.navy,'normal');
box_(axA,0.280,0.140,0.135,0.140,S.navy,1.2,pale);
txt_(axA,0.280,0.175,'H2',fs,S.text,'bold');
txt_(axA,0.280,0.112,sprintf('n = %d',nH2),fsn-1,S.navy,'normal');
% direction key, outside the flow
txt_(axA,0.760,0.185,'Q1, Q2:  train H1 → evaluate H2',fs-1,S.text,'normal');
txt_(axA,0.760,0.095,'Q3, Q4:  both split directions',fs-1,S.text,'normal');


% ================= Panel B =================
axB = axes('Parent',fig,'Units','normalized','Position',[0.035 0.040 0.945 0.230]);
hold(axB,'on'); axis(axB,[0 1 0 1]); axis(axB,'off');
qk = {'Q1','Q2','Q3','Q4'};
% Q3 wording is re-broken over the same four lines: 'Opposite-half vs same-sample' alone
% measures 45.3 mm at 9.5 pt against a 38.6 mm question box.
qt = {{'Configuration-','specific RATE/AUTOC','on independent','held-out evaluation'}, ...
      {'Paired incremental','RATE comparison'}, ...
      {'Opposite-half vs','same-sample model','development and','evaluation diagnostic'}, ...
      {'Preprocessing-','placement diagnostic','with opposite-half','model fitting'}};
w=0.235; g=0.012; x0=0.010;   % right edge 0.986 < 1.0 -> Q4 border not clipped
for k=1:4
    cx = x0 + (k-1)*(w+g) + w/2;
    box_(axB,cx,0.515,w,0.910,S.navy,1.1,pale);
    txt_(axB,cx,0.840,qk{k},fs,S.navy,'bold');   % comfortable padding under the top border
    lines = qt{k};
    y0 = 0.390 + (numel(lines)-1)*0.076;      % vertically centre the body block
    for j=1:numel(lines)
        txt_(axB,cx,y0-(j-1)*0.152,lines{j},9.5,S.text,'normal');
    end
end

annotation(fig,'textbox',[0.004 0.940 0.06 0.05],'String','(A)','FontName','Arial','FontWeight','bold', ...
  'FontSize',S.fpanel,'EdgeColor','none','Color',S.text,'FitBoxToText','on');
% (B) raised 2.0 mm (y 0.278 -> 0.2959 of the 111.9 mm canvas): at 600 dpi the parentheses of the old label
% reached the Q1 top edge (ink overlap ~0.15 mm); the ink gap is now ~1.85 mm while (B) stays ~5 mm below the
% H1/H2 boxes, i.e. clearly attached to panel B. x = 0.004 so that it left-aligns with (A).
annotation(fig,'textbox',[0.004 0.2959 0.06 0.05],'String','(B)','FontName','Arial','FontWeight','bold', ...
  'FontSize',S.fpanel,'EdgeColor','none','Color',S.text,'FitBoxToText','on');
jiim_export_r7(fig,'Fig1',outdir);

function box_(ax,cx,cy,w,h,edge,lw,face)
    rectangle(ax,'Position',[cx-w/2 cy-h/2 w h],'Curvature',0.16, ...
        'EdgeColor',edge,'LineWidth',lw,'FaceColor',face);
end
function txt_(ax,cx,cy,s,fsz,col,wt)
    text(ax,cx,cy,s,'FontName','Arial','FontSize',fsz,'Color',col, ...
        'HorizontalAlignment','center','VerticalAlignment','middle', ...
        'FontWeight',wt,'Interpreter','none');
end
function seg_(ax,x1,y1,x2,y2,col,lw)
    plot(ax,[x1 x2],[y1 y2],'-','Color',col,'LineWidth',lw);
end

