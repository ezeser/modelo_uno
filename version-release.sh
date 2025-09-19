#!/usr/bin/env bash
set -e

# 1️⃣ Asegurarse de tener las últimas referencias y tags
git fetch origin --tags

# 2️⃣ Detectar cambios en el proyecto
CHANGED=$(git status --short | awk '{print $2}')
if [ -z "$CHANGED" ]; then
  echo "⚠️ No hay cambios detectados. Nada que releasear."
  exit 1
fi

# 3️⃣ Pedir mensaje de commit
read -rp "📝 Escribe el mensaje de commit: " COMMIT_MSG

# 4️⃣ Obtener la última versión estable desde main/master
BASE_TAG=$(git describe --tags --abbrev=0 origin/master 2>/dev/null || echo "v1.0.0")
BASE_NUM=${BASE_TAG#v}
IFS='.' read -r MAJOR MINOR PATCH <<<"$BASE_NUM"

# 5️⃣ Generar nuevo tag PATCH+1
NEW_PATCH=$((PATCH + 1))
NEW_TAG="v${MAJOR}.${MINOR}.${NEW_PATCH}"

# 6️⃣ Mostrar resumen
echo ""
echo "🚀 Preparando release..."
echo "   Archivos a commitear:"
echo "$CHANGED" | sed 's/^/     • /'
echo "   Branch destino: master"
echo "   Commit:         $COMMIT_MSG"
echo "   Base tag:       $BASE_TAG"
echo "   Nuevo tag:      $NEW_TAG"
echo ""
read -rp "❓ ¿Proceder con estos cambios? (y/n): " CONFIRM
[ "$CONFIRM" = "y" ] || { echo "❌ Operación cancelada."; exit 1; }

# 7️⃣ Ejecutar commit y push
git add .
git commit -m "$COMMIT_MSG" || echo "⚠️ No hay cambios que commitear"
git push origin master

# 8️⃣ Crear y subir el nuevo tag
git tag "$NEW_TAG"
git push origin "$NEW_TAG"

echo "✅ Commit y tag $NEW_TAG publicados correctamente (branch master)."
