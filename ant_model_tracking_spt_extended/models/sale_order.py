from odoo import api, fields, models, _

class sale_order(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def write(self, vals):
        order_line_obj = self.env['sale.order.line']
        message_obj = self.env['mail.message']
        tracking_obj = self.env['mail.tracking.value']
        old_value = {}
        if 'order_line' in vals.keys():
            for order_line in self.order_line:
                old_value[order_line.id] = {
                    'product_id' : order_line.product_id,
                    'name' : order_line.name,
                    'discount': order_line.discount,
                    'price_tax': order_line.price_tax,
                    'price_total': order_line.price_total,
                    'price_subtotal': order_line.price_subtotal,
                    'product_uom_qty': order_line.product_uom_qty,
                }
        res = super(sale_order, self).write(vals)     
        models_ids_spt = eval(self.env['ir.config_parameter'].get_param('models_ids_spt', default='[]'))
        models_ids = self.env['ir.model'].search([('id','in',models_ids_spt)])
        models_name = []
        if models_ids:
            models_name = models_ids.mapped('model')
        if str(self._name) in models_name: 
            if 'order_line' in vals.keys():
                message_id = message_obj.create({
                            'type': 'notification',
                            'res_id': self.id,
                            'model': 'sale.order',
                       })
                tracked_fields = order_line_obj.fields_get()
                initial = False
                for order_line in vals['order_line']:

                    if len(order_line) >=3 and order_line[0] in [4,1] and order_line[2]:
                        initial = old_value[order_line[1]]
                        for col_name, col_info in tracked_fields.items():
                            if col_name in ['product_id','name','discount','price_tax','price_total','price_subtotal','product_uom_qty']:                            
                                initial_value = initial[col_name]
                                new_value = getattr(order_line_obj.browse(order_line[1]), col_name)
                                if new_value != initial_value and (new_value or initial_value): 
                                    tracking_dict = self.env['mail.tracking.value'].create_tracking_values(order_line.browse(initial_value[0]) if  isinstance(initial_value,tuple) else initial_value, new_value, col_name, col_info)
                                elif new_value == initial_value and col_name in tracked_fields:
                                    tracking_dict = self.env['mail.tracking.value'].create_tracking_values(order_line.browse(initial_value[0]) if  isinstance(initial_value,tuple) else initial_value, order_line.browse(initial_value[0]) if  isinstance(initial_value,tuple) else initial_value, col_name, col_info)        
                                tracking_dict['mail_message_id'] = message_id.id
                                tracking_obj.create(tracking_dict)
                            
                    if len(order_line)>=3 and order_line[0] == 0 and order_line[2]:
                        line_id = order_line_obj.search([('product_id','=',order_line[2]['product_id']),('order_id','=',self.id),('price_unit','=',order_line[2]['price_unit']),('product_uom_qty','=',order_line[2]['product_uom_qty'])],limit=1)
                        for col_name, col_info in tracked_fields.items():
                            if col_name in ['product_id','name','discount','price_tax','price_total','price_subtotal','product_uom_qty']:
                                new_value = getattr(line_id, col_name)
                                tracking_dict = self.env['mail.tracking.value'].create_tracking_values({},new_value,col_name, col_info)        

                                tracking_dict['mail_message_id'] = message_id.id
                                tracking_obj.create(tracking_dict)
                    
                    if len(order_line)>=2 and order_line[0] == 2 and order_line[1]:
                        initial = old_value[order_line[1]]
                        for col_name, col_info in tracked_fields.items():
                            if col_name in ['product_id','name','discount','price_tax','price_total','price_subtotal','product_uom_qty']:
                                initial_value = initial[col_name]

                                tracking_dict = self.env['mail.tracking.value'].create_tracking_values(initial_value,{},col_name, col_info)        

                                tracking_dict['mail_message_id'] = message_id.id
                                tracking_obj.create(tracking_dict)
        return res