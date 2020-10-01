from odoo import api, fields, models, _

class account_invoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def write(self, vals):
        invoice_line_obj = self.env['account.invoice.line']
        message_obj = self.env['mail.message']
        tracking_obj = self.env['mail.tracking.value']
        old_value = {}
        if 'invoice_line_ids' in vals.keys():
            for invoice_line_ids in self.invoice_line_ids:
                old_value[invoice_line_ids.id] = {
                    'product_id' : invoice_line_ids.product_id,
                    'name' : invoice_line_ids.name,
                    'invoice_line_tax_ids': invoice_line_ids.invoice_line_tax_ids,
                    'discount': invoice_line_ids.discount,
                    'price_subtotal': invoice_line_ids.price_subtotal,
                    'quantity': invoice_line_ids.quantity,
                }

        res = super(account_invoice, self).write(vals)     
        models_ids_spt = eval(self.env['ir.config_parameter'].get_param('models_ids_spt', default='[]'))
        models_ids = self.env['ir.model'].search([('id','in',models_ids_spt)])
        models_name = []
        if models_ids:
            models_name = models_ids.mapped('model')
        if str(self._name) in models_name: 
            if 'invoice_line_ids' in vals.keys():
                message_id = message_obj.create({
                            'type': 'notification',
                            'res_id': self.id,
                            'model': 'account.invoice',
                       })
                tracked_fields = invoice_line_obj.fields_get()
                initial = False
                for invoice_line_ids in vals['invoice_line_ids']:

                    if len(invoice_line_ids) >=3 and invoice_line_ids[0] in [4,1] and invoice_line_ids[2]:
                        initial = old_value[invoice_line_ids[1]]
                        for col_name, col_info in tracked_fields.items():
                            if col_name in ['product_id','name','invoice_line_tax_ids','discount','price_subtotal','quantity']:                            
                                initial_value = initial[col_name]
                                new_value = getattr(invoice_line_obj.browse(invoice_line_ids[1]), col_name)
                                if new_value != initial_value and (new_value or initial_value): 
                                    tracking_dict = self.env['mail.tracking.value'].create_tracking_values(invoice_line_ids.browse(initial_value[0]) if  isinstance(initial_value,tuple) else initial_value, new_value, col_name, col_info)
                                elif new_value == initial_value and col_name in tracked_fields:
                                    tracking_dict = self.env['mail.tracking.value'].create_tracking_values(invoice_line_ids.browse(initial_value[0]) if  isinstance(initial_value,tuple) else initial_value, invoice_line_ids.browse(initial_value[0]) if  isinstance(initial_value,tuple) else initial_value, col_name, col_info)        
                                if tracking_dict:
                                    tracking_dict['mail_message_id'] = message_id.id
                                    tracking_obj.create(tracking_dict)                            
                    if len(invoice_line_ids)>=3 and invoice_line_ids[0] == 0 and invoice_line_ids[2]:
                        line_id = invoice_line_obj.search([('product_id','=',invoice_line_ids[2]['product_id']),('invoice_id','=',self.id),('price_unit','=',invoice_line_ids[2]['price_unit']),('quantity','=',invoice_line_ids[2]['quantity'])],limit=1)
                        for col_name, col_info in tracked_fields.items():
                            if col_name in ['product_id','name','invoice_line_tax_ids','discount','price_subtotal','quantity']:
                                new_value = getattr(line_id, col_name)
                                tracking_dict = self.env['mail.tracking.value'].create_tracking_values({},new_value,col_name, col_info)        
                                if tracking_dict:
                                    tracking_dict['mail_message_id'] = message_id.id
                                    tracking_obj.create(tracking_dict)
                    
                    if len(invoice_line_ids)>=2 and invoice_line_ids[0] == 2 and invoice_line_ids[1]:
                        initial = old_value[invoice_line_ids[1]]
                        for col_name, col_info in tracked_fields.items():
                            if col_name in ['product_id','name','invoice_line_tax_ids','discount','price_subtotal','quantity']:
                                initial_value = initial[col_name]

                                tracking_dict = self.env['mail.tracking.value'].create_tracking_values(initial_value,{},col_name, col_info)        

                                if tracking_dict:
                                    tracking_dict['mail_message_id'] = message_id.id
                                    tracking_obj.create(tracking_dict)
        return res
