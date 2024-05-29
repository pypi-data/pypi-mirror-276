# ------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -------------------------------------------------------------------------

from azure.appconfiguration.provider import load, SettingSelector
from sample_utilities import get_client_modifications
import os

kwargs = get_client_modifications()
connection_string = os.environ["APPCONFIGURATION_CONNECTION_STRING"]

# Connecting to Azure App Configuration using connection string
config = load(connection_string=connection_string, **kwargs)

print(config["message"])
print(config["my_json"]["key"])

# Connecting to Azure App Configuration using connection string and trimmed key prefixes
trimmed = ["test."]
config = load(connection_string=connection_string, trim_prefixes=trimmed, **kwargs)

print(config["message"])

# Connection to Azure App Configuration using SettingSelector
selects = [SettingSelector(key_filter="message*")]
config = load(connection_string=connection_string, selects=selects, **kwargs)

print("message found: " + str("message" in config))
print("test.message found: " + str("test.message" in config))
