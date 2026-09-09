% make_Fig2.m — Q1: six standard centred doubly robust RATE/AUTOC estimates,
% independent held-out evaluation. Rendering source of truth. Class V.
S = jiim_style_r7();
here = fileparts(mfilename('fullpath'));
D = load(fullfile(here,'..','..','figure_data','fig_data_r7.mat'));
outdir = fullfile(here,'..','..','reproduction','figures');

est = D.f2_est(:); lo = D.f2_lo(:); hi = D.f2_hi(:);
labs = cellstr(D.labels); n = numel(est);
assert(n==6 && all(lo<=est) && all(est<=hi), 'Fig2 canonical data failed the ordering check');

fig = figure('Color',[1 1 1],'Units','centimeters','Position',[2 2 S.width_cm 10.6]);
ax = axes('Parent',fig,'Units','normalized','Position',[0.365 0.155 0.605 0.795]);
hold(ax,'on');
y = n:-1:1;                                    % row 1 at the top
xline(ax,0,':','Color',S.zero,'LineWidth',1.0);
for i = 1:n
    plot(ax,[lo(i) hi(i)],[y(i) y(i)],'-','Color',S.dark,'LineWidth',S.ci_lw);
end
% every configuration carries one identical navy filled marker: equal visual status
h = plot(ax,est,y,'o','MarkerSize',S.mk_fill,'MarkerFaceColor',S.navy, ...
         'MarkerEdgeColor',S.text,'LineWidth',S.mk_edge,'LineStyle','none');
set(ax,'YLim',[0.45 n+0.55]);
xlim(ax,[-0.26 0.26]); set(ax,'XTick',-0.2:0.1:0.2);
jiim_ylabels_r7(ax,y,labs,S);
xlabel(ax,'RATE (AUTOC)','FontName','Arial','FontSize',S.faxis,'Color',S.text,'Interpreter','none');
jiim_axes_r7(ax,S);
jiim_export_r7(fig,'Fig2',outdir);
