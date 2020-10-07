# -*- coding: utf-8 -*-
# Part of ANT. See LICENSE file for full copyright and licensing details.
from odoo import SUPERUSER_ID, models, fields, api
from odoo import tools
import pytz
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import logging

class Message(models.Model):
    _inherit = 'mail.message'
    
    @api.multi
    def _notify(self, force_send=False, send_after_commit=True, user_signature=True):
        context = self.env.context.copy()
        context['mail_notify_author'] = True
        self = self.with_context(context)
        return super(Message,self)._notify(force_send,send_after_commit,user_signature)
    
class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    @api.multi
    def _notify(self, message, force_send=False, send_after_commit=True, user_signature=True):
        # TDE TODO: model-dependant ? (like customer -> always email ?)
        message_sudo = message.sudo()
        email_channels = message.channel_ids.filtered(lambda channel: channel.email_send)
        print(self.ids)
        self.sudo().search([
            '|',
            ('id', 'in', self.ids),
            ('channel_ids', 'in', email_channels.ids),
            ('notify_email', '!=', 'none')])._notify_by_email(message, force_send=force_send, send_after_commit=send_after_commit, user_signature=user_signature)
#         self.sudo().search([
#             '|',
#             ('id', 'in', self.ids),
#             ('channel_ids', 'in', email_channels.ids),
#             ('email', '!=', message_sudo.author_id and message_sudo.author_id.email or message.email_from),
#             ('notify_email', '!=', 'none')])._notify_by_email(message, force_send=force_send, send_after_commit=send_after_commit, user_signature=user_signature)
        self._notify_by_chat(message)
        return True
