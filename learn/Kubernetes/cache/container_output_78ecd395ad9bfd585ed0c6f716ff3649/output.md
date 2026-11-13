<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The manifests in `templates/` must be namespace-level objects. It's best to avoid using CRDs if you can. If you must use CRDs, you need to place them in `crds/` instead and none of those CRDs can be templates. Helm will apply those CRDs before it renders and applies templates.

Why should you avoid CRDs? Recall that CRDs are cluster-level objects. That means that if you ...

 * update a CRD, all objects under it will change as well regardless of what namespace they're under.
 * delete a CRD, all objects under it will delete as well regardless of what namespace they're under.

Imagine having two installs of some chart, where each install is a different version of the chart. Those installs are under their own name and namespace combinations, but they're sharing the same CRDs. If a newer version of a chart modifies / deletes a CRD, installing it may mess up installs of older versions of that chart. For that reason, Helm ignores updates and deletes to CRDs in `/crds`.
</div>

