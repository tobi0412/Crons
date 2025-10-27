#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para ejecutar el scraper de FUTBIN
"""

import asyncio
import nodriver as uc
from scraping.main import main

if __name__ == "__main__":
    uc.loop().run_until_complete(main())

