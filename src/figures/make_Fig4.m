% make_Fig4.m — Q3: change in the RATE point estimate under same-sample versus opposite-half
% model development/evaluation. Descriptive; no interval, no p-value. Class V.
S = jiim_style_r7();
here = fileparts(mfilename('fullpath'));
D = load(fullfile(here,'..','..','figure_data','fig_data_r7.mat'));
outdir = fullfile(here,'..','..','reproduction','figures');

H1 = D.f4_H1(:); H2 = D.f4_H2(:); PO = D.f4_pooled(:);
labs = cellstr(D.labels); n = numel(PO);
assert(all(H1>0) && all(H2>0) && all(PO>0), 'Fig4: all 18 Q3 values must be positive');

fig = figure('Color',[1 1 1],'Units','centimeters','Position',[2 2 S.width_cm 11.9]);
ax = axes('Parent',fig,'Units','normalized','Position',[0.365 0.255 0.605 0.695]);
hold(ax,'on');
y = n:-1:1; off = 0.19;
xline(ax,0,':','Color',S.zero,'LineWidth',1.0);
for i = 1:n     % half-specific range within the row only; never across configurations
    plot(ax,[H1(i) H2(i)],[y(i)+off y(i)-off],'-','Color',S.conn,'LineWidth',1.1);
end
h1 = plot(ax,H1,y+off,'o','MarkerSize',S.mk_open,'MarkerFaceColor','none', ...
          'MarkerEdgeColor',S.dark,'LineWidth',S.mk_edge,'LineStyle','none');
h2 = plot(ax,H2,y-off,'^','MarkerSize',S.mk_open,'MarkerFaceColor','none', ...
          'MarkerEdgeColor',S.medium,'LineWidth',S.mk_edge,'LineStyle','none');
h3 = plot(ax,PO,y,'o','MarkerSize',S.mk_fill,'MarkerFaceColor',S.navy, ...
          'MarkerEdgeColor',S.text,'LineWidth',S.mk_edge,'LineStyle','none');
set(ax,'YLim',[0.42 n+0.58]);
xlim(ax,[-0.035 0.45]); set(ax,'XTick',0:0.1:0.4);
jiim_ylabels_r7(ax,y,labs,S);
% two-line label: the single line 'Change in RATE (same-sample − opposite-half)' measures 115.6 mm
% and ends at the 173.8 mm canvas edge (0.0 mm margin); the first line keeps the previous label position.
xlabel(ax,{'Change in RATE','(same-sample − opposite-half)'},'FontName','Arial', ...
       'FontSize',S.faxis,'Color',S.text,'Interpreter','none');
jiim_axes_r7(ax,S);
% legend generated from the ACTIVE plotted handles only (no orphan entries)
hs = [h1 h2 h3];
nm = {sprintf('H1 (n = %d)',D.nH1), sprintf('H2 (n = %d)',D.nH2), 'Pooled'};
keep = arrayfun(@(g) ~isempty(get(g,'XData')), hs);
lg = legend(ax,hs(keep),nm(keep),'Orientation','horizontal','FontName','Arial', ...
            'FontSize',S.ftick,'Box','off','TextColor',S.text);
lg.Units = 'normalized'; lg.Position = [0.395 0.022 0.545 0.052];
jiim_export_r7(fig,'Fig4',outdir);
