#!/bin/bash

# Safety default: do not push tags unless explicitly opted in.
if [ "${BMV_PUSH_TAGS:-false}" = "true" ]; then
	git push --tags
else
	echo "Skipping tag push. Set BMV_PUSH_TAGS=true to enable."
fi
