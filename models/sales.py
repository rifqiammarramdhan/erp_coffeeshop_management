from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)



class kedai_kopi_sales(models.Model):
    _name = "kedai.kopi.sales"


    # Generate Sequence And Button open
    def func_set_to_open(self):
        if self.status == 'draft':
            if self.name == "New":
                seq = self.env['ir.sequence'].next_by_code('kedai.kopi.sales') or 'New'
                self.name = seq
                self.status = 'open'

    # Set To Paid
    def func_set_to_paid(self):
        if self.status == 'open':
            self.status = 'paid'

    name = fields.Char(string="PO Number", default="New",readonly=True)
    customer = fields.Char(string='Customer')
    date = fields.Date(string="Date")
    status = fields.Selection([("draft","Draft"),("open","Open"),("paid","Paid")], default="draft")
    kedai_kopi_sales_invoice_ids = fields.One2many('kedai.kopi.sales.invoice', 'kedai_kopi_sales_invoice_id', string="kedai Kopi Inventory Category Ids")


class kedai_kopi_sales_invoice(models.Model):
    _name = "kedai.kopi.sales.invoice"

    # @api.onchange('product_id')
    # def funct_onchange_unitPrice(self):
    #     if not self.product_id:
    #         self.unitPrice = 0.0
    #     else:
    #         _logger.error('Creating a new record with valuesssss: %s', self.product_id.sale_price)
    #         self.unitPrice = self.product_id.sale_price
    #         # self.unitPrice = 9999999999.0

    @api.onchange('product_id')
    def funct_onchange_unit_price(self):
        if self.product_id:
            self.unitPrice = self.product_id.sale_price
            return {}
        else:
            self.unitPrice = 0.0

    @api.depends("quantity")
    def _compute_amount(self):
        for item in self:
            if item.product_id:
                item.amount = item.quantity * item.product_id.sale_price
            else:
                item.amount = 0.0

    @api.depends("taxes", "amount")
    def _compute_tax_amount(self):
        for item in self:
            tax_percent = item.taxes / 100
            item.tax_amount = item.amount * tax_percent


    @api.depends("tax_amount", "amount")
    def _compute_total(self):
        for item in self:
            item.total = item.amount + item.tax_amount


    # Fields
    kedai_kopi_sales_invoice_id = fields.Many2one('kedai.kopi.sales', string="Kedai Kopi Sales Id")
    # Many To One
    product_id = fields.Many2one('kedai.kopi.inventory.item', string="Product")
    quantity = fields.Integer(string='Quantity', default=0,store=True,require=True)
    taxes = fields.Float(string='Taxes', default=0,store=True)
    amount = fields.Float(string='Amount', compute=_compute_amount,store=True,readonly=True)
    tax_amount = fields.Float(string='Tax Amount', compute=_compute_tax_amount,store=True,readonly=True)
    total = fields.Float(string='Total', compute=_compute_total,store=True,readonly=True)
    unitPrice = fields.Float(string="Price", store=True)





