import uno
# from CellInsertMode import NO_SHIFT

def format_columns_and_freeze_header():
    desktop = XSCRIPTCONTEXT.getDesktop()
    model = desktop.getCurrentComponent()
    sheet = model.CurrentController.ActiveSheet
    cell_range = sheet.getCellRangeByName("A1:Z1")
    cell_range.freezeAtPosition(1, 0)
    cell_range.setPropertyValue("IsCellBackgroundTransparent", False)
    cell_range.setPropertyValue("CellBackColor", 13421823)
    cell_range.setPropertyValue("HoriJustify", uno.getConstantByName("com.sun.star.table.CellHoriJustify.CENTER"))
    cell_range.setPropertyValue("VertJustify", uno.getConstantByName("com.sun.star.table.CellVertJustify.CENTER"))
    sheet.Columns[0].Width = 2000