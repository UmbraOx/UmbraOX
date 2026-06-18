class ResponseFormatter:

    def format(
        self,
        prompt=None,
        proposals=None,
        domains=None,
        verified=True,
        deployment_safe=True,
        data=None
    ):

        # BACKWARD COMPATIBILITY
        # Allows:
        # format({...})
        # format(prompt=...)
        # format(old_response)

        if (
            isinstance(prompt, dict)
            and data is None
        ):
            data = prompt

        if data:

            prompt = data.get(
                "prompt",
                prompt
            )

            proposals = data.get(
                "proposals",
                proposals
            )

            domains = data.get(
                "domains",
                domains
            )

            verified = data.get(
                "verified",
                verified
            )

            deployment_safe = data.get(
                "deployment_safe",
                deployment_safe
            )

        if proposals is None:
            proposals = []

        if domains is None:
            domains = []

        lines = []

        lines.append("")
        lines.append(
            "========================================"
        )

        lines.append(
            "UMBRA RESPONSE"
        )

        lines.append(
            "========================================"
        )

        lines.append("")

        lines.append(
            f"Prompt: {prompt}"
        )

        lines.append("")
        lines.append(
            "PROPOSALS"
        )

        lines.append(
            "---------"
        )

        if not proposals:

            lines.append(
                "- No proposals generated"
            )

        for index, proposal in enumerate(
            proposals,
            start=1
        ):

            if not isinstance(
                proposal,
                dict
            ):
                continue

            lines.append(
                f"[{index}] "
                f"{proposal.get('title')}"
            )

            lines.append(
                f"    Type: "
                f"{proposal.get('type')}"
            )

            lines.append(
                f"    Target: "
                f"{proposal.get('target')}"
            )

            lines.append("")

        lines.append(
            "DOMAINS"
        )

        lines.append(
            "-------"
        )

        if not domains:

            lines.append(
                "- none"
            )

        for domain in domains:

            lines.append(
                f"- {domain}"
            )

        lines.append("")
        lines.append(
            f"Runtime Verified: "
            f"{verified}"
        )

        lines.append(
            f"Deployment Safe: "
            f"{deployment_safe}"
        )

        lines.append("")

        return "\n".join(lines)