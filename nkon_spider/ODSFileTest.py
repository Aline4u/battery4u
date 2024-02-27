import jpype
import asposecells
jpype.startJVM()


from asposecells.api import Workbook


# load_options = LoadOptions(FileFormatType.CSV)

# Create an instance of the Workbook class.
workbook = Workbook()

# Insert the words Hello World! into a cell accessed.
workbook.getWorksheets().get(0).getCells().get("A1").putValue("Hello World")

# Save as XLS file
workbook.save("output.xls")

# Save as XLSX file
workbook.save("output.xlsx")

# Save as ods file
workbook.save("output.ods")

jpype.shutdownJVM()
