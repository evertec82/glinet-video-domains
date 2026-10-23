# GL.iNet video domains

One GL.iNet-compatible, domain-only subscription for major video services. It combines and deduplicates maintained upstream rules for YouTube, Netflix, X/Twitter, TikTok, Facebook/Instagram, Prime Video, Disney+, Hulu, Max/HBO, and Peacock.

## Subscription URL

After publishing, use:

```text
https://raw.githubusercontent.com/evertec82/glinet-video-domains/main/dist/video-domains.txt
```

In GL.iNet, choose the VPN policy based on a specified domain/IP list, select **Subscription URL**, paste the raw URL, and run **Detect**. This list contains one lowercase domain per line and no IP ranges.

## Updating

GitHub Actions rebuilds the list daily at 06:23 UTC and commits only when content changes. Run it locally with Python 3.9+:

```sh
python -m unittest discover -v
python scripts/build.py
```

The build fails if an upstream disappears, changes to an unsupported format, or produces no valid domains.

## Sources and attribution

- [marcomc/glinet-vpn-subscription-lists](https://github.com/marcomc/glinet-vpn-subscription-lists) supplies GL.iNet-ready YouTube and Meta domains (MIT; its generated data carries upstream-specific terms documented by that project).
- [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) supplies Clash YAML rules for the other named services (GPL-2.0 and repository-specific notices).

This repository transforms and aggregates factual domain entries; it does not imply endorsement by the services or upstream maintainers. Review upstream licenses/notices before redistribution. Domains can be shared across services or CDNs, so routing may affect traffic beyond video playback. Service IP traffic, hard-coded DNS, QUIC behavior, and firmware-specific matching can also require separate configuration.

