from odoo import api, fields, models, _

class account_move(models.Model):
    _name = 'account.move'
    _inherit = ['account.move','mail.thread', 'ir.needaction_mixin']

    @api.multi
    def write(self, vals):
        move_line_obj = self.env['account.move.line']
        message_obj = self.env['mail.message']
        tracking_obj = self.env['mail.tracking.value']
        old_value = {}
        if 'line_ids' in vals.keys():
            for line_ids in self.line_ids:
                old_value[line_ids.id] = {
                    'product_id' : line_ids.product_id,
                    'name' : line_ids.name,
                    'tax_ids': line_ids.tax_ids,
                    'partner_id': line_ids.partner_id,
                    'account_id': line_ids.account_id,
                    'quantity': line_ids.quantity,
                    'debit' : line_ids.debit,
                    'credit' : line_ids.credit,
                    'move_id' : line_ids.move_id,
                }

        res = super(account_move, self).write(vals)     
        models_ids_spt = eval(self.env['ir.config_parameter'].get_param('models_ids_spt', default='[]'))
        models_ids = self.env['ir.model'].search([('id','in',models_ids_spt)])
        models_name = []
        if models_ids:
            models_name = models_ids.mapped('model')
        if str(self._name) in models_name: 
            if 'line_ids' in vals.keys():
                message_id = message_obj.create({
                            'type': 'notification',
                            'res_id': self.id,
                            'model': 'account.move',
                       })
                tracked_fields = move_line_obj.fields_get()
                initial = False
                for line_ids in vals['line_ids']:

                    if len(line_ids) >=3 and line_ids[0] in [4,1] and line_ids[2]:
                        initial = old_value[line_ids[1]]
                        for col_name, col_info in tracked_fields.items():
                            if col_name in ['product_id','name','debit','move_id','credit','tax_ids','partner_id','account_id','quantity']:                            
                                initial_value = initial[col_name]
                                new_value = getattr(move_line_obj.browse(line_ids[1]), col_name)
                                if new_value != initial_value and (new_value or initial_value): 
                                    tracking_dict = self.env['mail.tracking.value'].create_tracking_values(line_ids.browse(initial_value[0]) if  isinstance(initial_value,tuple) else initial_value, new_value, col_name, col_info)
                                elif new_value == initial_value and col_name in tracked_fields:
                                    tracking_dict = self.env['mail.tracking.value'].create_tracking_values(line_ids.browse(initial_value[0]) if  isinstance(initial_value,tuple) else initial_value, line_ids.browse(initial_value[0]) if  isinstance(initial_value,tuple) else initial_value, col_name, col_info)        
                                if tracking_dict:
                                    tracking_dict['mail_message_id'] = message_id.id
                                    tracking_obj.create(tracking_dict)                            
                    if len(line_ids)>=3 and line_ids[0] == 0 and line_ids[2]:
                        line_id = move_line_obj.search([('product_id','=',line_ids[2]['product_id']),('move_id','=',self.id),('price_unit','=',line_ids[2]['price_unit']),('quantity','=',line_ids[2]['quantity'])],limit=1)
                        for col_name, col_info in tracked_fields.items():
                            if col_name in ['product_id','name','debit','move_id','credit','tax_ids','partner_id','account_id','quantity']:
                                new_value = getattr(line_id, col_name)
                                tracking_dict = self.env['mail.tracking.value'].create_tracking_values({},new_value,col_name, col_info)        
                                if tracking_dict:
                                    tracking_dict['mail_message_id'] = message_id.id
                                    tracking_obj.create(tracking_dict)
                    
                    if len(line_ids)>=2 and line_ids[0] == 2 and line_ids[1]:
                        initial = old_value[line_ids[1]]
                        for col_name, col_info in tracked_fields.items():
                            if col_name in ['product_id','name','debit','move_id','credit','tax_ids','partner_id','account_id','quantity']:
                                initial_value = initial[col_name]

                                tracking_dict = self.env['mail.tracking.value'].create_tracking_values(initial_value,{},col_name, col_info)        

                                if tracking_dict:
                                    tracking_dict['mail_message_id'] = message_id.id
                                    tracking_obj.create(tracking_dict)
        return res
