from odoo import api, fields, models, _


class base_config_settings(models.TransientModel):
    _inherit = 'base.config.settings'


    models_ids_spt = fields.Many2many('ir.model','models_base_config_real_spt','model_id','config_id','Models')


    @api.onchange('models_ids_spt')
    def onchange_analytic_accounting(self):
        self.env['ir.config_parameter'].set_param('models_ids_spt',self.models_ids_spt.ids)
    
    @api.model
    def get_default_all(self, fields):
        models_ids_spt = self.env['ir.config_parameter'].get_param('models_ids_spt', default='[]')
        return dict(models_ids_spt=[(6,0,eval(models_ids_spt))])
