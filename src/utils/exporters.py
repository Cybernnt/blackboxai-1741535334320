c.save()
            return True
        except Exception as e:
            return False, str(e)

    @staticmethod
    def export_to_excel(data, file_path):
        """Export data to Excel file"""
        try:
            import openpyxl
            wb = openpyxl.Workbook()
            ws = wb.active
            
            for row in data:
                ws.append(row)
                
            wb.save(file_path)
            return True
        except Exception as e:
            return False, str(e)
