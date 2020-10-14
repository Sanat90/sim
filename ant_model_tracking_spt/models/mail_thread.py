import pytz
from odoo import api, fields, models, _
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT


class mail_thread(models.AbstractModel):
    _inherit = 'mail.thread'
    
    def check_time_zone(self,t_date):
        t_date = str(t_date)   
        print(t_date)   
#         t_date = str(t_date.replace(tzinfo=None)) 
#         print(t_date)    
        if len(t_date) > 20:
            n = 20 # chunk length
            t_date_val = t_date[0:19]
            t_date = t_date_val
        dt_value = t_date
        if t_date:
            timez = 'Asia/Singapore'
            if self._context and 'tz' in self._context and self._context.get('tz') != False:
                timez = self._context.get('tz')
            rec_date_from  = datetime.strptime(t_date, DEFAULT_SERVER_DATETIME_FORMAT)
#             print(timez)
            src_tz = pytz.timezone('UTC')
            dst_tz = pytz.timezone(timez)
            src_dt = src_tz.localize(rec_date_from, is_dst=True)
            print(src_dt)
            dt_value = src_dt.astimezone(dst_tz)
            dt_value = dt_value.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
            print(dt_value)
        return dt_value
    

    @api.multi
    def _message_track(self, tracked_fields, initial):
        """ For a given record, fields to check (tuple column name, column info)
            and initial values, return a structure that is a tuple containing :

            - a set of updated column names
            - a list of changes (initial value, new value, column name, column info) """
            
        models_ids_spt = eval(self.env['ir.config_parameter'].get_param('models_ids_spt', default='[]'))
        models_ids = self.env['ir.model'].search([('id','in',models_ids_spt)])
        models_name = []
        if str(self._name) in models_name:
            models_name = models_ids.mapped('model')        
        self.ensure_one()
        changes = set()  # contains always and onchange tracked fields that changed
        displays = set()  # contains always tracked field that did not change but displayed for information
        tracking_value_ids = []
        display_values_ids = []
        if models_ids_spt:
            for col_name, col_info in tracked_fields.items():
                track_visibility = getattr(self._fields[col_name], 'track_visibility', False)
                initial_value = initial[col_name]
                new_value = getattr(self, col_name)
                if col_info['type'] in ['datetime']:
                    if new_value:
#                         new_utc_value = self.locatize_time(new_value)
                        new_value = self.check_time_zone(new_value)
                print(new_value)
                if new_value != initial_value and (new_value or initial_value):  # because browse null != False
                    tracking = self.env['mail.tracking.value'].create_tracking_values(initial_value, new_value, col_name, col_info)
                    if tracking:
                        tracking_value_ids.append([0, 0, tracking])

                    if col_name in tracked_fields:
                        changes.add(col_name)
                # 'always' tracked fields in separate variable; added if other changes
                elif new_value == initial_value and track_visibility == 'always' and col_name in tracked_fields:
                    tracking = self.env['mail.tracking.value'].create_tracking_values(initial_value, initial_value, col_name, col_info)
                    if tracking:
                        display_values_ids.append([0, 0, tracking])
                        displays.add(col_name)

            if changes and displays:
                tracking_value_ids = display_values_ids + tracking_value_ids

            return changes, tracking_value_ids

        else:
            
            # generate tracked_values data structure: {'col_name': {col_info, new_value, old_value}}
            for col_name, col_info in tracked_fields.items():
                track_visibility = getattr(self._fields[col_name], 'track_visibility', 'onchange')
                initial_value = initial[col_name]
                new_value = getattr(self, col_name)
                
                if col_info['type'] in ['datetime']:
                    if new_value:
#                         new_utc_value = self.locatize_time(new_value)
                        new_value = self.check_time_zone(new_value)

                if new_value != initial_value and (new_value or initial_value):  # because browse null != False
                    tracking = self.env['mail.tracking.value'].create_tracking_values(initial_value, new_value, col_name, col_info)
                    if tracking:
                        tracking_value_ids.append([0, 0, tracking])

                    if col_name in tracked_fields:
                        changes.add(col_name)
                # 'always' tracked fields in separate variable; added if other changes
                elif new_value == initial_value and track_visibility == 'always' and col_name in tracked_fields:
                    tracking = self.env['mail.tracking.value'].create_tracking_values(initial_value, initial_value, col_name, col_info)
                    if tracking:
                        display_values_ids.append([0, 0, tracking])
                        displays.add(col_name)

            if changes and displays:
                tracking_value_ids = display_values_ids + tracking_value_ids

            return changes, tracking_value_ids
    
    @api.model
    def _get_tracked_fields(self, updated_fields):
        """ Return a structure of tracked fields for the current model.
            :param list updated_fields: modified field names
            :return dict: a dict mapping field name to description, containing
                always tracked fields and modified on_change fields
        """
        models_ids_spt = eval(self.env['ir.config_parameter'].get_param('models_ids_spt', default='[]'))
        models_ids = self.env['ir.model'].search([('id','in',models_ids_spt)])
        models_name = []
        if models_ids:
            models_name = models_ids.mapped('model')
        if str(self._name) in models_name:
            tracked_fields = []
            for name, field in self._fields.items():
                tracked_fields.append(name)
            if tracked_fields:
                return self.fields_get(tracked_fields)
            # return self.fields_get(updated_fields)
            return {}
        else:
            tracked_fields = []
            for name, field in self._fields.items():
                if getattr(field, 'track_visibility', False):
                    tracked_fields.append(name)

            if tracked_fields:
                return self.fields_get(tracked_fields)
            return {}