% make_Fig3.m — Q2: (A) clinical-only vs reference held-out RATE; (B) paired dRATE forest.
% Panel-B navy marks the PREDEFINED PRIMARY INFERENTIAL CONTRAST, not a historical status. Class V.
S = jiim_style_r7();
here = fileparts(mfilename('fullpath'));
D = load(fullfile(here,'..','..','figure_data','fig_data_r7.mat'));
outdir = fullfile(here,'..','..','reproduction','figures');

aE=D.f3a_est(:); aL=D.f3a_lo(:); aH=D.f3a_hi(:); aLab=cellstr(D.f3a_lab);
bE=D.f3b_est(:); bL=D.f3b_lo(:); bH=D.f3b_hi(:); bLab=cellstr(D.f3b_lab);
assert(numel(aE)==2 && numel(bE)==5,'Fig3 canonical data has the wrong row counts');
assert(all(aL<=aE) && all(aE<=aH) && all(bL<=bE) && all(bE<=bH),'Fig3 interval ordering failed');

fig = figure('Color',[1 1 1],'Units','centimeters','Position',[2 2 S.width_cm 12.6]);

% ---- Panel A ----
axA = axes('Parent',fig,'Units','normalized','Position',[0.365 0.760 0.605 0.185]);
hold(axA,'on'); yA=[2 1];
xline(axA,0,':','Color',S.zero,'LineWidth',1.0);
plot(axA,aE,yA,'-','Color',S.conn,'LineWidth',1.1);          % one paired comparison
for i=1:2, plot(axA,[aL(i) aH(i)],[yA(i) yA(i)],'-','Color',S.dark,'LineWidth',S.ci_lw); end
plot(axA,aE,yA,'o','MarkerSize',S.mk_fill,'MarkerFaceColor',S.navy, ...
     'MarkerEdgeColor',S.text,'LineWidth',S.mk_edge,'LineStyle','none');
set(axA,'YLim',[0.45 2.55]);
xlim(axA,[-0.26 0.26]); set(axA,'XTick',-0.2:0.1:0.2);
jiim_ylabels_r7(axA,yA,aLab,S);
xlabel(axA,'RATE (AUTOC)','FontName','Arial','FontSize',S.faxis,'Color',S.text,'Interpreter','none');
jiim_axes_r7(axA,S);

% ---- Panel B ----
axB = axes('Parent',fig,'Units','normalized','Position',[0.365 0.125 0.605 0.430]);
hold(axB,'on'); n=5; yB=n:-1:1;
xline(axB,0,':','Color',S.zero,'LineWidth',1.0);
for i=1:n
    c = S.dark; if i==1, c = S.dark; end
    plot(axB,[bL(i) bH(i)],[yB(i) yB(i)],'-','Color',c,'LineWidth',S.ci_lw);
end
plot(axB,bE(2:end),yB(2:end),'o','MarkerSize',S.mk_fill,'MarkerFaceColor',S.medium, ...
     'MarkerEdgeColor',S.text,'LineWidth',S.mk_edge,'LineStyle','none');
plot(axB,bE(1),yB(1),'o','MarkerSize',S.mk_fill,'MarkerFaceColor',S.navy, ...
     'MarkerEdgeColor',S.text,'LineWidth',S.mk_edge,'LineStyle','none');
set(axB,'YLim',[0.45 n+0.55]);
xlim(axB,[-0.20 0.40]); set(axB,'XTick',-0.2:0.1:0.4);
jiim_ylabels_r7(axB,yB,bLab,S);
xlabel(axB,'Difference in RATE','FontName','Arial','FontSize',S.faxis,'Color',S.text,'Interpreter','none');
jiim_axes_r7(axB,S);

annotation(fig,'textbox',[0.018 0.938 0.06 0.055],'String','(A)','FontName','Arial', ...
  'FontWeight','bold','FontSize',S.fpanel,'EdgeColor','none','Color',S.text,'FitBoxToText','on');
annotation(fig,'textbox',[0.018 0.575 0.06 0.055],'String','(B)','FontName','Arial', ...
  'FontWeight','bold','FontSize',S.fpanel,'EdgeColor','none','Color',S.text,'FitBoxToText','on');
jiim_export_r7(fig,'Fig3',outdir);
