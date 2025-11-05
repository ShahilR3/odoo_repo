from odoo import models, fields

class ProductProduct(models.Model):
    _inherit = 'product.product'

    x_custom_note = fields.Char(
        string='Custom Note',
        help='This is a custom note field for the product.'
    )
