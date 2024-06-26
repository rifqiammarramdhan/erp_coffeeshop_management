from odoo import models, fields, api, _


class kedai_kopi_inventory_category(models.Model):
    _name = 'kedai.kopi.inventory.category'

    name = fields.Char(string="Name")
    unit = fields.Integer(string="Unit", compute='_compute_total_produk', store=True)

    # Field untuk Relasi | One to Many
    kedai_kopi_inventory_category_ids = fields.One2many('kedai.kopi.inventory.item', 'kedai_kopi_inventory_category_id',
                                                        string="kedai Kopi Inventory Category Ids")

    @api.depends('kedai_kopi_inventory_category_ids.unit')
    def _compute_total_produk(self):
        for category in self:
            item_count = len(category.kedai_kopi_inventory_category_ids)
            category.unit = item_count


class kedai_kopi_inventory_item(models.Model):
    _name = 'kedai.kopi.inventory.item'

    @api.depends('quantity_incoming', 'quantity_outgoing')
    def _compute_total_unit(self):
        for item in self:
            total_unit = item.unit  # Pastikan total_unit memiliki nilai awal yang valid
            # Tambahkan quantity_incoming ke total_unit
            if item.quantity_incoming:
                total_unit += item.quantity_incoming

            # Kurangkan quantity_outgoing dari total_unit
            if item.quantity_outgoing:
                total_unit -= item.quantity_outgoing

            item.total_unit = total_unit

    product_ids = fields.One2many('kedai.kopi.sales.invoice', 'product_id', string="Product")
    kedai_kopi_inventory_category_id = fields.Many2one('kedai.kopi.inventory.category',
                                                       string="Kedai Kopi Inventory Category Item Id")

    name = fields.Char(string="Name", default="New")
    description = fields.Char(string="Description")
    unit = fields.Integer(string="Unit")
    total_unit = fields.Integer(string="Total Unit", compute='_compute_total_unit', store=True, readonly=True)
    cost = fields.Float(string="Cost")
    sale_price = fields.Float(string="Sale Price")
    status = fields.Char(string="Status")
    quantity_incoming = fields.Integer(string="Quantity Incoming")
    quantity_outgoing = fields.Integer(string="Quantity Outgoing")

    # Bidang kategori yang terkait dengan nama kategori pada model kedai_kopi_inventory_category
    category = fields.Char(string="Category", related='kedai_kopi_inventory_category_id.name', readonly=True)
