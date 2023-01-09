import base64
import io

from odoo import models, _
from PIL import Image


class ReportPlanLegal(models.AbstractModel):
    _name = 'report.report_cerro_stock'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        
        format26_c_bold = workbook.add_format(
            {'font_size': 14, 'bg_color': '#A0A0A0', 'align': 'center', 'valign': 'vcenter', 'bold': True, 'text_wrap': True, 'border': 1})
        format21_left = workbook.add_format(
            {'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'bold': False, 'text_wrap': True, 'border': 1})
        format21_gray = workbook.add_format(
            {'font_size': 10, 'bg_color': '#EEEEEE', 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'border': 1})
        format21_gray_bold = workbook.add_format(
            {'font_size': 10, 'bg_color': '#EEEEEE', 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'bold': True, 'border': 1})

        product_ids = self.env['product.product'].browse(data['product_ids']) if data['product_ids'] else self.env['product.product'].search([])
        from_date = data['from_date']
        to_date = data['to_date']

        # Report 1: Categoría	Producto	Descripción	Unidad	Cantidad
        if data['type'] == 'report_1':
            sheet = workbook.add_worksheet(_('Stock report without lost'))
            sheet.set_column(0, 4, 20)
            sheet.write(0, 0, 'Categoría', format26_c_bold)
            sheet.write(0, 1, 'Producto', format26_c_bold)
            sheet.write(0, 2, 'Descripción', format26_c_bold)
            sheet.write(0, 3, 'Unidad', format26_c_bold)
            sheet.write(0, 4, 'Cantidad', format26_c_bold)
            row = 1
            for product in product_ids:
                sheet.write(row, 0, product.categ_id.name, format21_left)
                sheet.write(row, 1, product.name, format21_left)
                sheet.write(row, 2, product.description, format21_left)
                sheet.write(row, 3, product.uom_id.name, format21_left)
                sheet.write(row, 4, product.qty_available - product.product_lost_state_qty, format21_left)
                row += 1
        
        # Report 2: Categoría	Producto	Descripción	Unidad	Bueno	Regular	Malo	Perdido	Cantidad total
        if data['type'] == 'report_2':
            sheet = workbook.add_worksheet(_('Stock report by state'))
            sheet.set_column(0, 8, 20)
            sheet.write(0, 0, 'Categoría', format26_c_bold)
            sheet.write(0, 1, 'Producto', format26_c_bold)
            sheet.write(0, 2, 'Descripción', format26_c_bold)
            sheet.write(0, 3, 'Unidad', format26_c_bold)
            sheet.write(0, 4, 'Bueno', format26_c_bold)
            sheet.write(0, 5, 'Regular', format26_c_bold)
            sheet.write(0, 6, 'Malo', format26_c_bold)
            sheet.write(0, 7, 'Perdido', format26_c_bold)
            sheet.write(0, 8, 'Cantidad total', format26_c_bold)
            row = 1
            for product in product_ids:
                sheet.write(row, 0, product.categ_id.name, format21_left)
                sheet.write(row, 1, product.name, format21_left)
                sheet.write(row, 2, product.description, format21_left)
                sheet.write(row, 3, product.uom_id.name, format21_left)
                sheet.write(row, 4, product.product_good_state_qty, format21_left)
                sheet.write(row, 5, product.product_regular_state_qty, format21_left)
                sheet.write(row, 6, product.product_bad_state_qty, format21_left)
                sheet.write(row, 7, product.product_lost_state_qty, format21_left)
                sheet.write(row, 8, product.qty_available, format21_left)
                row += 1

        # Report 3: Categoría	Producto	Descripción	Unidad	Ubicación (dentro de almacén)*	Anaquel o código*	Cantidad
        if data['type'] == 'report_3':
            sheet = workbook.add_worksheet(_('Stock report by location'))
            sheet.set_column(0, 6, 20)
            sheet.write(0, 0, 'Categoría', format26_c_bold)
            sheet.write(0, 1, 'Producto', format26_c_bold)
            sheet.write(0, 2, 'Descripción', format26_c_bold)
            sheet.write(0, 3, 'Unidad', format26_c_bold)
            sheet.write(0, 4, 'Ubicación (dentro de almacén)*', format26_c_bold)
            sheet.write(0, 5, 'Anaquel o código*', format26_c_bold)
            sheet.write(0, 6, 'Cantidad', format26_c_bold)
            row = 1
            for product in product_ids:
                sheet.write(row, 0, product.categ_id.name, format21_left)
                sheet.write(row, 1, product.name, format21_left)
                sheet.write(row, 2, product.description, format21_left)
                sheet.write(row, 3, product.uom_id.name, format21_left)
                sheet.write(row, 4, product.location_id.name, format21_left)
                sheet.write(row, 5, product.shelf, format21_left)
                sheet.write(row, 6, product.qty_available, format21_left)
                row += 1

        # Report 4: Categoría	Producto	Descripción	Unidad	Cantidad Zona 1	Cantidad Zona 2	Cantidad Zona 3	Cantidad total
        if data['type'] == 'report_4':
            sheet = workbook.add_worksheet(_('Stock report by location and zone'))
            sheet.set_column(0, 7, 20)
            sheet.write(0, 0, 'Categoría', format26_c_bold)
            sheet.write(0, 1, 'Producto', format26_c_bold)
            sheet.write(0, 2, 'Descripción', format26_c_bold)
            sheet.write(0, 3, 'Unidad', format26_c_bold)
            # map locations of all products
            locations = self.env['stock.location'].search([('usage', '=', 'internal')])
            # write locations in header
            col = 4
            for location in locations:
                sheet.write(0, col, location.name, format26_c_bold)
                col += 1
            sheet.write(0, col, 'Cantidad total', format26_c_bold)
            row = 1
            for product in product_ids:
                sheet.write(row, 0, product.categ_id.name, format21_left)
                sheet.write(row, 1, product.name, format21_left)
                sheet.write(row, 2, product.description, format21_left)
                sheet.write(row, 3, product.uom_id.name, format21_left)
                col = 4
                for location in locations:
                    location_open_quants = self.env['stock.quant'].search([('product_id', '=', product.id), ('location_id', '=', location.id)])
                    sheet.write(row, col, sum([quant.available_quantity for quant in location_open_quants]), format21_left)
                    col += 1
                sheet.write(row, col, product.qty_available - product.product_lost_state_qty, format21_left)
                row += 1

        # Reporte 5	Categoría	Producto	Descripción	Unidad	Cantidad
        if data['type'] == 'report_5':
            sheet = workbook.add_worksheet(_('Stock report only lost'))
            sheet.set_column(0, 4, 20)
            sheet.write(0, 0, 'Categoría', format26_c_bold)
            sheet.write(0, 1, 'Producto', format26_c_bold)
            sheet.write(0, 2, 'Descripción', format26_c_bold)
            sheet.write(0, 3, 'Unidad', format26_c_bold)
            sheet.write(0, 4, 'Cantidad', format26_c_bold)
            row = 1
            for product in product_ids:
                sheet.write(row, 0, product.categ_id.name, format21_left)
                sheet.write(row, 1, product.name, format21_left)
                sheet.write(row, 2, product.description, format21_left)
                sheet.write(row, 3, product.uom_id.name, format21_left)
                sheet.write(row, 4, product.product_lost_state_qty, format21_left)
                row += 1
        
        # Report 6 only saleable:	Categoría	Producto	Descripción	Unidad	Cantidad (excluye malo o perdido)	Precio (referencial)	Impuesto
        if data['type'] == 'report_6':
            product_ids = product_ids.filtered(lambda x: x.sale_ok)
            sheet = workbook.add_worksheet(_('Stock report only saleable'))
            sheet.set_column(0, 6, 20)
            sheet.write(0, 0, 'Categoría', format26_c_bold)
            sheet.write(0, 1, 'Producto', format26_c_bold)
            sheet.write(0, 2, 'Descripción', format26_c_bold)
            sheet.write(0, 3, 'Unidad', format26_c_bold)
            sheet.write(0, 4, 'Cantidad (excluye malo o perdido)', format26_c_bold)
            sheet.write(0, 5, 'Precio (referencial)', format26_c_bold)
            sheet.write(0, 6, 'Impuesto', format26_c_bold)
            row = 1
            for product in product_ids:
                sheet.write(row, 0, product.categ_id.name, format21_left)
                sheet.write(row, 1, product.name, format21_left)
                sheet.write(row, 2, product.description, format21_left)
                sheet.write(row, 3, product.uom_id.name, format21_left)
                sheet.write(row, 4, product.qty_available - product.product_bad_state_qty - product.product_lost_state_qty, format21_left)
                sheet.write(row, 5, product.standard_price, format21_left)
                sheet.write(row, 6, product.taxes_id.name, format21_left)
                row += 1
        
        # Report 7: Producto	Fecha	Cantidad disponible	Cantidad actualizada
        # get stock in to_date and from_date
        if data['type'] == 'report_7':
            sheet = workbook.add_worksheet(_('Stock report moves by date and products'))
            sheet.set_column(0, 3, 20)
            sheet.write(0, 0, 'Producto', format26_c_bold)
            sheet.write(0, 1, 'Fecha', format26_c_bold)
            sheet.write(0, 2, 'Cantidad disponible', format26_c_bold)
            sheet.write(0, 3, 'Cantidad actualizada', format26_c_bold)
            row = 1
            # get product quantity in to_date
            for product in product_ids:
                sheet.write(row, 0, product.name, format21_left)
                sheet.write(row, 1, data['to_date'], format21_left)
                sheet.write(row, 2, product.with_context({'to_date': from_date}).qty_available, format21_left)
                sheet.write(row, 3, product.with_context({'to_date': to_date}).qty_available, format21_left)
                row += 1
        
        # Report 8: ID de movimiento	Producto	Fecha	Medida	Cantidad	Persona	Bueno	Regular	Malo	Ubicación de origen	Ubicación de destino
        if data['type'] == 'report_8':
            sheet = workbook.add_worksheet(_('Stock report internal moves'))
            sheet.set_column(0, 10, 20)
            sheet.write(0, 0, 'ID de movimiento', format26_c_bold)
            sheet.write(0, 1, 'Producto', format26_c_bold)
            sheet.write(0, 2, 'Fecha', format26_c_bold)
            sheet.write(0, 3, 'Medida', format26_c_bold)
            sheet.write(0, 4, 'Cantidad', format26_c_bold)
            sheet.write(0, 5, 'Persona', format26_c_bold)
            sheet.write(0, 6, 'Bueno', format26_c_bold)
            sheet.write(0, 7, 'Regular', format26_c_bold)
            sheet.write(0, 8, 'Malo', format26_c_bold)
            sheet.write(0, 9, 'Ubicación de origen', format26_c_bold)
            sheet.write(0, 10, 'Ubicación de destino', format26_c_bold)
            row = 1
            stock_move_line_ids = self.env['stock.move.line'].search([('product_id', 'in', product_ids.ids), ('date', '>=', from_date), ('date', '<=', to_date)])
            for stock_move_line in stock_move_line_ids:
                sheet.write(row, 0, stock_move_line.id, format21_left)
                sheet.write(row, 1, stock_move_line.product_id.name, format21_left)
                sheet.write(row, 2, stock_move_line.date, format21_left)
                sheet.write(row, 3, stock_move_line.product_uom_id.name, format21_left)
                sheet.write(row, 4, stock_move_line.qty_done, format21_left)
                sheet.write(row, 5, stock_move_line.picking_id.partner_id.name, format21_left)
                sheet.write(row, 6, stock_move_line.move_id.product_good_state_qty, format21_left)
                sheet.write(row, 7, stock_move_line.move_id.product_regular_state_qty, format21_left)
                sheet.write(row, 8, stock_move_line.move_id.product_bad_state_qty, format21_left)
                sheet.write(row, 9, stock_move_line.location_id.name, format21_left)
                sheet.write(row, 10, stock_move_line.location_dest_id.name, format21_left)
                row += 1


            
        
