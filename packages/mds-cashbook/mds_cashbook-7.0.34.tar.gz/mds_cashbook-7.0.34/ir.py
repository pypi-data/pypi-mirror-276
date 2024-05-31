# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds.de for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from trytond.transaction import Transaction
from trytond.pool import PoolMeta


class Rule(metaclass=PoolMeta):
    __name__ = 'ir.rule'

    @classmethod
    def _context_modelnames(cls):
        """ list of models to add 'user_id' to context
        """
        return [
            'cashbook.book', 'cashbook.line', 'cashbook.recon',
            'cashbook.split']

    @classmethod
    def _get_context(cls, model_name):
        context = super()._get_context(model_name)
        if model_name in cls._context_modelnames():
            context['user_id'] = Transaction().user
        return context

    @classmethod
    def _get_cache_key(cls, model_name):
        key = super()._get_cache_key(model_name)
        if model_name in cls._context_modelnames():
            key = (*key, Transaction().user)
        return key

# end Rule
